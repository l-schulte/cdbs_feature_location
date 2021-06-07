echo 0001
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 0
echo 0010
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 10
echo 0100
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 100
echo 0500
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 500
echo 1000
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 1000
echo 0001
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 0
echo 0010
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 10
echo 0100
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 100
echo 0500
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 500
echo 1000
python3.8 -u app.py -t lda pa -e lda pa -v lda pa -i tmp/ --lda_k1 350 --pa_k1 100 --pa_k2 100 --iterations 100 --burn_in 1000

