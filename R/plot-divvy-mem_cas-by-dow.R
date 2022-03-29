#
# there must already be a loaded divvy dataset
#

library(dplyr)
library(ggplot2)

remove(dow)
gc()
divvy

#
# get divvy summary for member, casual by day_of_week
#
remove(agg)
remove(dba)

# aggregate, get a count for member/casual by dow
agg <- aggregate(divvy$ID, by=list(divvy$member_casual,divvy$day_of_week), FUN=length)
agg # see what we've got
# reshape
dba <- reshape(agg, idvar="Group.1", timevar="Group.2", direction='wide')
dba # see it
row.names(dba) <- dba$Group.1  # set row names to member/casual
dba <- dba[, 2:ncol(dba)] # drop first col, which was member/casual

#update the column names
colnames(dba) <- c("Friday", 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday')
dba
# change the order of the columns
dba <- dba[, c(2, 6, 7, 5, 1, 3, 4)]
dba # see it
fwrite(dba, 'd:/DivvyDatasets/member-casual-by-dow.csv', row.names = TRUE)

# now need a matrix
dbam <- data.matrix(dba)
dbam
barplot(dbam, beside=TRUE, main="Rides by Member/Casual on a Given Day",
        col=c("yellow","darkblue"),
        axes = FALSE,
        legend.text=rownames(dbam),

                args.legend = list(x='topright' 
                           )
        )


# make a data matrix -- nneded?
#aggm <- data.matrix(agg)
#aggm

#
# simple bar plot of the totals by month
#  members_start is the top 20 starting stations,
#  with a total in the last row
#
mat <- data.matrix(members_start)
barplot(mat[21,], col="blue", ylab="Count", main="Member Rides from Top 20 Stations")

mat2 <- data.matrix(casual_start)
barplot(mat2[21,], col="orange", ylab="Count", main="Casual Rides from Top 20 Stations")

