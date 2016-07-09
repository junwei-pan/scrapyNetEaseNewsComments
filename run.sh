# Put the following line to the crontab -e
# 0 */6 * * * sh /home/ubuntu/Github/scrapyNetEaseNewsComments/run.sh > /home/ubuntu/Github/scrapyNetEaseNewsComments/log/crontab.log
DATE=`date`
dir="/home/ubuntu/Github/scrapyNetEaseNewsComments"
log="$dir/log/run.log"
cmd="/usr/local/bin/scrapy crawl stack_crawler"

cd $dir
echo "$DATE"
echo "Run new crawler at $DATE" >> $log
eval "$cmd" >> $log
