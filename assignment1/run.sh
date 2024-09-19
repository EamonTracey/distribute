programs=$(ls | grep -E "^Test([0-9]|10)\.py$" | sort -n)

for program in $programs; do
    echo $program
    for _ in $(seq 1 10); do
        python3 $program
    done
    echo
done
