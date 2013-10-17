#!/bin/bash
function pause(){
    echo ""
   read -p "Press [enter] to continue..."
   echo ""
}

echo "$ csvlook gsm.csv"
csvlook gsm.csv | head -n 20
echo "..."
pause

echo "$ csvcut -c name gsm.csv | tail -n +2"
csvcut -c name gsm.csv | tail -n +2 | head -n 20
echo "..."
pause

echo "$csvgrep -c state -m new gsm.csv | csvcut -c name,state | csvlook"
csvgrep -c state -m new gsm.csv | csvcut -c name,state | csvlook | head -n 20
echo "..."
pause