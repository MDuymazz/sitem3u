name: Run txt_to_m3u.py script

on:
  workflow_run:
    workflows: ["Run verileri_birlestir.py script"]  # Ana Domain workflow'u tamamlandığında çalışacak
    types:
      - completed
  workflow_dispatch:  # Manuel olarak çalıştırılabilir
jobs:
  run_base_url_script:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python environment
        uses: actions/setup-python@v3  # Daha güncel versiyon kullanıyoruz
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip

      - name: Run txt_to_m3u.py
        run: |
          python txt_to_m3u.py

      # Ana link dosyasını kontrol ediyoruz
      - name: Check if gol.m3u is updated
        id: check_update
        run: |
          echo "Checking if gol.m3u was updated:"
          cat gol.m3u  # Dosyanın içeriğini kontrol ediyoruz
          
          OLD_URL=$(cat gol.m3u)
          NEW_URL=$(python txt_to_m3u.py)  # Yeni URL'yi almak için scripti çalıştırıyoruz
          
          if [ "$OLD_URL" == "$NEW_URL" ]; then
            echo "URL güncellemeye gerek yoktur"
            echo "no_update=true" >> $GITHUB_ENV  # URL değişmemişse environment variable set ediyoruz
          else
            echo "URL başarıyla gol.m3u dosyasına güncellendi"
            echo "no_update=false" >> $GITHUB_ENV  # URL güncellenmişse farklı bir variable set ediyoruz
          fi

      # GitHub Actions'a yapılan değişiklikleri commit ediyoruz
      - name: Commit updated gol.m3u
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"

          # Değişiklik olup olmadığını kontrol et
          git pull  # Güncel değişiklikleri almak için ekledik
          if git diff --quiet; then
            echo "No changes detected. Skipping commit."
          else
            git add gol.m3u
            if [ "${{ env.no_update }}" == "true" ]; then
              git commit -m "Mac Verileri güncellenmeye gerek yoktur"
            else
              git commit -m "Tamamlandı."
            fi
            git push
          fi
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      
