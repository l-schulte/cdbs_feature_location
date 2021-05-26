echo LDA
echo alpha_0.01
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 350 -i /tmp --burn_in 0 --iterations 100 --alpha 0.01
echo alpha_0.1
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 350 -i /tmp --burn_in 0 --iterations 100 --alpha 0.1
echo alpha_1
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 350 -i /tmp --burn_in 0 --iterations 100 --alpha 1
echo alpha_10
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 350 -i /tmp --burn_in 0 --iterations 100 --alpha 10
echo eta_0.01
python3.8 -u app.py -t lda -e lda -v lda --lda_k1 350 -i /tmp --burn_in 0 --iterations 100 --eta 0.01
echo eta_0.1
python3.8 -u app.py -t lda -e lda -v lda --lda_k1 350 -i /tmp --burn_in 0 --iterations 100 --eta 0.1
echo eta_1
python3.8 -u app.py -t lda -e lda -v lda --lda_k1 350 -i /tmp --burn_in 0 --iterations 100 --eta 1
echo eta_10
python3.8 -u app.py -t lda -e lda -v lda --lda_k1 350 -i /tmp --burn_in 0 --iterations 100 --eta 10
echo PA
echo alpha_0.01
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --alpha 0.01
echo alpha_0.1
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --alpha 0.1
echo alpha_1
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --alpha 1
echo alpha_10
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --alpha 10
echo sub_alpha_0.01
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --sub_alpha 0.01
echo sub_alpha_0.1
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --sub_alpha 0.1
echo sub_alpha_1
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --sub_alpha 1
echo sub_alpha_10
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --sub_alpha 10
echo eta_0.01
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --eta 0.01
echo eta_0.1
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --eta 0.1
echo eta_1
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --eta 1
echo eta_10
python3.8 -u app.py -t pa -e pa -v pa --pa_k1 100 --pa_k2 100 -i /tmp --burn_in 100 --iterations 100 --eta 10
