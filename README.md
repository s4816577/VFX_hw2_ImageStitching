# VFX_hw2_ImageStitching
b03902028 ¼B«Û§Ê b03902029 §õ«T½å
1. How to run our Code
cd to src\
type (remember the input image sequence must be scene-left to scene-right)
python main.py --files ..\images\001.JPG ..\images\002.JPG ..\images\003.JPG ..\images\004.JPG ..\images\005.JPG ..\images\006.JPG ..\images\007.JPG ..\images\008.JPG ..\images\009.JPG ..\images\010.JPG ..\images\011.JPG ..\images\012.JPG ..\images\013.JPG ..\images\014.JPG ..\images\015.JPG ..\images\016.JPG ..\images\017.JPG ..\images\018.JPG ..\images\019.JPG ..\images\020.JPG ..\images\021.JPG ..\images\022.JPG ..\images\023.JPG ..\images\024.JPG ..\images\025.JPG ..\images\026.JPG --focallength 961.974
wait for 10~20 min
it will output stitched_image.png in the current folder

2. Implementation Detail
2.1 Feature Detection
We use Harris corner detector to find feature points on images. To restrict the number of feature points, we adopt an naive non-maximal supression method.

We start picking point from high response. When we find that one of the neighbor of the point we want to pick was already picked, we skip this point. By doing so, we have high quality and well distributed feature points.

We use the 9x9 patch with feature point as center to describe the corresponding feature point.

2.2 Feature Matching
We use kd-tree, which professor mentioned in class, to quickly find match feature points.

To let the works more precisely, we assumed that user should input images with left-to-right order, and by this assumption we forced our matching point¡¦s x should be more than half of image¡¦s width to match the next image.

At the end of matching, we forced that for each point p¡¦s first and second best match¡¦s distance d1/d2 should be less than 0.95 to ensure the point is specific enough.

2.3 Cylindrical Warping
We project images and feature points onto a cylindrical surface. Since all image are taken with a fixed center, we can expect that translation will be the only transform on this cylindrical coordinate.

Also, don¡¦t forget to warp those feature points and let the center of the image to be the warping-origin as well.

2.4 RANSAC
In this part, we do basically same as the algorithm which professor teached.



2.5 Transition Calculation
Beacuse of using tripod, we basically only consider the transition between images. The following is the transition model we used. Where xi yi are the image_left¡¦s matched feature, xi¡¦ yi¡¦ are image_right¡¦s matched feature, and dx dy are those transition on x-axis and y-axis.


We slove this by Least-square approximation.

2.6 Blending
At the end, we use linear blending to blend overlap regions, which is also the one professor mentioned in class.


3. Our Result
Please reference to HTML in this repo.

4. Reference
Richard Szeliski, Image Alignment and Stitching: A Tutorial, Foundations and Trends in Computer Graphics and Vision, 2006
R. Szeliski and H.-Y. Shum. Creating full view panoramic image mosaics and texture-mapped models, SIGGRAPH 1997, pp251-258.
VFX2011 Edwardhw & Tantofish
(http://www.cmlab.csie.ntu.edu.tw/~tantofish/course/vfx/report/stitching.html)