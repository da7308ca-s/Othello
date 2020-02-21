coord_walkers = [[4,4]]*8
for i in range(8):
	print("in")
	print(coord_walkers[0][0])
	coord_walkers[0][0]=coord_walkers[0][0]-1 #up

	coord_walkers[1][0]-=1 #up right
	coord_walkers[1][1]+=1 #up right

	coord_walkers[2][1]+=1 #right

	coord_walkers[3][0]+=1 #down right
	coord_walkers[3][1]+=1 #down right

	coord_walkers[4][0]+=1 #down

	coord_walkers[5][0]+=1 #down left
	coord_walkers[5][1]-=1 #down left

	coord_walkers[6][1]-=1 #left

	coord_walkers[7][0]-=1 #up left
	coord_walkers[7][1]-=1 #up left
print(coord_walkers)