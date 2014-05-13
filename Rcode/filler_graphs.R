paper_counts = data.frame('Princeton University' = 7013,
                    'Harvard University' = 10578,
                    'Yale University' = 16283,
                    'Brown University' = 3090,
                    'Columbia University' = 12039,
                    'Cornell University' = 5588,
                    'Dartmouth College' = 1796,
                    'University of Pennsylvania' = 10651)

p_counts = c(7013, 10578, 16283, 3090, 12039, 5588, 1796, 10651)
names(p_counts) = c("Princeton","Harvard","Yale","Brown","Columbia","Cornell","Dartmouth","UPenn")
barplot(p_counts, col='lavender', las=3,mai=c(4,4,4,4), main="Published Graduate Theses\n (on ProQuest)")

pops = c(2674,14000,6809,1947,18568,8004,1950,11028)
barplot(p_counts/pops, col='blue', las=3, mai=c(4,4,4,4),main="Theses per current student\n (on ProQuest)")
