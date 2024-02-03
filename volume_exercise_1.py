import numpy as np
import open3d

from sklearn.cluster import KMeans
from scipy.spatial import ConvexHull


def visualize_open3d(pts):
    # check if the point cloud array is in the right shape.
    shape = pts.shape
    if shape[1] == 3:
        pass
    else:
        pts = np.transpose(pts)
    pc = open3d.geometry.PointCloud()
    pc.points = open3d.utility.Vector3dVector(pts)
    
    # Visualize in open3d
    open3d.visualization.draw_geometries([pc])
    # open3d.visualization.draw_geometries([pc, coord_frame])

def get_object_volume_from_pointcloud(points):

    # Task: Get the volume of the object, which appears to be a cylinder so vol = pi * r^2 * h

    # Idea: can use clustering to seperate object from the flat surface

    # Get the cluster centers (min and max y values, in column index 2)
    # (I'm assuming the object is the one with the higher y values, since it's placed on top of the surface,
    #  so I'm using the min and max y values as the starting points for the cluster centers)
    cluster_centers = np.array([[np.min(points[:,2])], [np.max(points[:,2])]]).reshape(-1,1)

    # KMeans model
    kmeans = KMeans(n_clusters=2, init=cluster_centers, n_init=1)
    kmeans.fit(points[:,2].reshape(-1,1))

    # Get points for object with higher y values (should be the second cluster, since the starting points are the min and max y values)
    object_points = points[kmeans.labels_ == 1]

    # Get the mean (can use this to help remove pesky outliers)
    mean = np.mean(object_points, axis=0)

    # Calculate the distance of each point from the mean
    distances = np.linalg.norm(object_points - mean, axis=1)

    # Remove points that are more than 2 standard deviations away from the mean
    object_points = object_points[distances < 2*np.std(distances)]

    # Final Approach: Using a Convex Hull (I thought this approach was better than the original approach below, since it could (potentially) handle shapes that are not cylindrical, 
    # like a sphere for example, where the other approach relies on the object being a cylinder shape). 
    # Also, the original approach has horrible runtime and my computer could not even begin to handle it.

    # Get points for the convex hull
    hull = ConvexHull(object_points)

    # The volume gets calculated automatically, so can just use the volume attribute. Seems to be in m^3 so need to convert to cm^3
    volume = hull.volume * 1000000

    # Visualize the convex hull (for debugging / testing)
    # visualize_open3d(object_points[hull.vertices])
    # print("Volume of the object: ", volume, "cm^3")

    return volume # Return the volume in cm^3

if __name__ == "__main__":
    # Load in Point Clouds - (x,y,z) coordinate points in meters
    points = np.load("data/PointCloud_143122066753.npy")

    # TODO: Estimate the volume of the object
    volume = get_object_volume_from_pointcloud(points)

    # Visualize in Open3D
    visualize_open3d(points)
    
    
# Context for my original approach that went up in flames (runtime was bad, thus not a good approach so I looked for an alternative)
# =================================================================================================================================================================
    
# Below is code for the original approach I tried using Pythagoras' Theorem by finding the max distance between points in the point cloud (after isolating the object from the surface)
# using that value as the hypotenuse for a triangle with other sides being the radius and height of the cylinder.
# I did not use this approach in the end, mainyl because it had a horrible runtime.
    
# =================================================================================================================================================================
    # # Get the biggest distance between two individual points -- that's the cylinder's diagonal
    # max_distance = 0
    # chunk_size = 1000
    # for i in range(0, len(object_points), chunk_size):
    #     for j in range(i, len(object_points), chunk_size):
    #         distances = np.linalg.norm(object_points[i:i+chunk_size] - object_points[j:j+chunk_size][:, None], axis=-1)
    #         max_distance = max(max_distance, np.max(distances))
    # diagonal = max_distance


    # # The max height value  minus the min height value  is the cylinder's radius
    # radius = np.max(object_points[:,2]) - np.min(object_points[:,2])

    # # Now just use good ol' Pythagoras  (where length^2 * radius^2 = diagonal^2)
    # length = np.sqrt(diagonal**2 - radius**2)

    # # Now that we have all three variables, can get an estimate of volume
    # volume = np.pi * radius**2 * length

    # print(volume)
# =================================================================================================================================================================