# Import PCL module
import pcl

# Load Point Cloud file
cloud = pcl.load_XYZRGB('tabletop.pcd')


# Voxel Grid filter
vox = cloud.make_voxel_grid_filter()
LEAF_SIZE = 0.01
vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
cloud_filtered = vox.filter()
filename = 'voxel_downsampled.pcd'
pcl.save(cloud_filtered, filename)


# PassThrough filter
# Creating the filter
passthrough = cloud_filtered.make_passthrough_filter()
# Assigning axis and range to the filter object
filter_axis = 'z'
passthrough.set_filter_field_name(filter_axis)
axis_min = 0.6
axis_max = 1.1
passthrough.set_filter_limits(axis_min, axis_max)
# Use the filter function to obtain resultant point
cloud_filtered = passthrough.filter()
filename = 'pass_through_filtered.pcd'
pcl.save(cloud_filtered, filename)


# RANSAC plane segmentation
# Creating object
seg = cloud_filtered.make_segmenter()
# Setting model
seg.set_model_type(pcl.SACMODEL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)
# Setting max_distance for segmenting the table
max_distance = 0.01
seg.set_distance_threshold(max_distance)
# Call segment function to obtain inlier indices and model coefficients
inliers, coefficients = seg.segment()


# Extract inliers
extracted_inliers = cloud_filtered.extract(inliers, negative=False)
filename = 'extracted_inliers.pcd'
pcl.save(extracted_inliers, filename)


# Extract outliers
extracted_outliers = cloud_filtered.extract(inliers, negative=True)
filename = 'extracted_outliers.pcd'
pcl.save(extracted_outliers, filename)
# Create the outlier filter
outlier_filter = cloud_filtered.make_statistical_outlier_filter()
# Set the number of neighboring points
outlier_filter.set_mean_k(50)
# Set threshold scale factor
x = 1.0
# Point with mean distance larger than global is outlier
outlier_filter.set_std_dev_mul_thresh(x)
# Calling filter
cloud_filtered = outlier_filter.filter()


# Save pcd for tabletop objects
filename = 'filtered_outliers.pcd'
pcl.save(cloud_filtered, filename)

