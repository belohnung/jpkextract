touch output.jpk

for file in *.split*; do
 cat "$file" >> output.jpk
done