#!/bin/bash


((amount=201079/10000))
((amount=amount+1))
echo $amount

sed -i 's/ Fwd Header Length.1/Fwd Header Length 2/g' TFTP_mini4.json

i=1
while [ $i -le $amount ]
do
	#echo $i
	((a=$i*20000))
	b="TFTP_Small$i.json"
	head -n $a TFTP_mini4.json | tail -n 20000 > $b
	#echo $b
	curl -k -X POST 'https://admin:admin@localhost:9200/_bulk?pretty' --data-binary @$b -H 'Content-Type: application/json'
	((i++))
done

echo "i am done"

