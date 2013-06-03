#/bin/sh
mysqldump -u$1 -p$1 $1 > backup-`eval date +%Y%m%d_%H%M%S`.sql
