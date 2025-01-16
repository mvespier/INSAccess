#!/bin/bash

date=$1
depart=$2
fichier=$3

curl "http://agendas.insa-rouen.fr/2024/day.php?cpath=&getdate=$date&cal%5B%5D=$depart" |
perl -pe 's/.*new EventData\(.*?\{(.*)\}.*/=TOTO=>$1/' |
grep "=TOTO=>" |
perl -pe 's/.*"display_start\\";s:\d+:\\"(.*?)\\".*"display_end\\";s:\d+:\\\"(.*?)\\".*"event_text\\";s:\d+:\\\"(.*?)\\".*"description\\";s:\d+:\\\".*?%2F%3E.*?%2F%3E.*?%2F%3E(.*?)%3C.*?\\".*"location\\";s:\d+:\\\"(.*?)\\".*/$1\t$2\t$3\t$4\t$5\t/' | 
sed "s/^/$date\t$depart\t/" > $fichier