The approach I ended up going with is as follows:
- Use KMeans clustering with the aim of seperating the flat surface points from the object points
    - For the KMeans clustering, start with 2 clusters -- one at the "bottom" of the point cloud, based on the assumptions that we know it is likely the surface (since in the real world, the object cannot just phase through the surface), and one at the "top" of the point cloud, which we know is likely the object given the surface it's on is flat.
- Use a convex hull to calculate the volume of the cluster of object points
- Convert the volume to the appropriate units and return it

Resources used:

- YouTube (I originally watched a video on DBSCAN, as I had not learned about it before, but ended up going with KMeans)
- I got the idea of using a convex hull to calculate the volume of the cluster from https://stackoverflow.com/questions/70186755/calculate-the-volume-of-cloud-points-of-a-tree-in-python after some Googling
- sklearn docs
- GitHub Copilot helped with some of the code particularly for writing KMeans with sklearn 
    (I have learned about KMeans before in terms of the use cases and algorithm from https://course.elementsofai.com/ but have not had to implement it in code before)

Other notes: 
- I tried DBSCAN at first instead of KMeans, but ended up going with KMeans for performance
- Instead of using a convex hull, I attempted using the max distance between two points as a proxy for the hypotenuse of a triangle with sides a, b, c where a and b would be the radius and height of the object, but abandoned this because a.) I would guess it would be less accurate and b.) getting the max distance between two points in a cluster is O(n^2) and I figured that would not be performant for large point clouds