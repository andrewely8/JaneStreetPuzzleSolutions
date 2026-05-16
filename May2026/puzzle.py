import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

board = [
	[0,0,21,0,0,0,0,0,0],
	[21,0,0,0,27,0,0,25,0],
	[0,27,0,0,0,15,0,0,9],
	[0,0,0,0,0,0,0,0,0],
	[25,0,0,27,0,45,0,0,9],
	[0,0,0,0,0,0,0,0,0],
	[9,0,0,63,0,0,0,45,0],
	[0,63,0,0,9,0,0,0,288],
	[0,0,0,0,0,0,35,0,0]
]

colors = [
	[1,0,0,1,0,1,0,1,0],
	[0,0,0,1,0,0,1,0,1],
	[1,0,0,0,0,0,0,1,0],
	[0,0,0,0,0,0,0,0,1],
	[1,0,0,0,1,0,0,0,0],
	[0,0,0,0,0,0,0,1,1],
	[0,0,0,0,0,0,0,0,0],
	[1,0,0,0,0,0,0,0,0],
	[0,1,0,0,1,0,1,0,1]
]

final_board = []

for i in range(len(board)):
	temp_board = []
	for j in range(len(board[i])):
		color = (0.70,1,0.7) if colors[i][j] == 1 else "white"
		num = None if board[i][j] == 0 else board[i][j]
		temp_board.append({"cv":"none", "color": color, "val":num})
	final_board.append(temp_board)                      
	
	
print(final_board[0])


def visual(arr,num_rows=9,num_cols=9,cell_size=16,cell_color='white',edge_color='black'):
	ax = plt.gca()

	for i in range(num_cols):
		for j in range(num_rows):

			rect = plt.Rectangle([j*16, i*16], cell_size, cell_size,facecolor=arr[i][j]['color'],edgecolor=edge_color)
			ax.add_patch(rect)
			plt.text(j*16+8,i*16+8, arr[i][j]['val'],fontsize="12",ha="center")

	ax.axis('off')
	ax.autoscale_view()
	ax.invert_yaxis()
	ax.set_aspect('equal', 'box')
	ax.xaxis.set_major_locator(plt.NullLocator())
	ax.yaxis.set_major_locator(plt.NullLocator())
	plt.show()



visual(final_board)










