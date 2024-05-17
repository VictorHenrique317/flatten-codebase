mkdir temp
find back/functions/src -type f -exec cp --backup=numbered -t temp/ {} +
find front/src -type f -exec cp --backup=numbered -t temp/ {} +
rm temp/*.ico
cd temp
cat ./* > codebase.txt
find . -type f ! -name "codebase.txt" -exec rm -f {} +
pandoc codebase.txt -o codebase.md
mv codebase.md ..
cd ..
rm -rf temp