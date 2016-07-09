DATE=`date`
dir="/home/ubuntu/Github/scrapyNetEaseNewsComments"
log="$dir/log/run.log"
cmd="/usr/local/bin/scrapy crawl stack_crawler"

cd $dir
echo "$DATE"
echo "Run new crawler at $DATE" >> $log
eval "$cmd" >> $log
