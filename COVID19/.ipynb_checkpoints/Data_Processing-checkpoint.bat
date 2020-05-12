cd C:/Users/KhacM/GitHub/MinhLe/COVID19/JohnHopkinsData
git merge origin/master --allow-unrelated-histories
git pull https://github.com/CSSEGISandData/COVID-19

cd C:/Users/KhacM/GitHub/MinhLe/COVID19
py "C:/Users/KhacM/GitHub/COVID-19/DataProcessing.py"

git add .
git commit -m "Updates"
git push

pause