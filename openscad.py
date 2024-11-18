import base64

import requests
import json

OPENSCAD_DOCS = ''' 
=== cube ===
----
Creates a cube or rectangular prism (i.e., a "box") in the first [[w:Octant_(solid_geometry)|octant]]. When center is true, the cube is centered on the origin. Argument names are optional if given in the order shown here.
 cube(size = [x,y,z], center = true/false);
 cube(size =  x ,     center = true/false);

: parameters:

:: size 
::: single value, cube with all sides this length
::: 3 value array [x,y,z], rectangular prism with dimensions x, y and z.
::  center
::: false (default), 1st (positive) octant, one corner at (0,0,0)
::: true, cube is centered at (0,0,0)

 default values:  cube();   yields:  cube(size = [1, 1, 1], center = false);
: examples:

[[File:OpenSCAD example Cube.jpg|150px]]

 equivalent scripts for this example
  cube(size = 18);
  cube(18);
  cube([18,18,18]);
  .
  cube(18,false);
  cube([18,18,18],false);
  cube([18,18,18],center=false);
  cube(size = [18,18,18], center = false);
  cube(center = false,size = [18,18,18] );

[[File:OpenSCAD example Box.jpg|150px]]

 equivalent scripts for this example
  cube([18,28,8],true);
  box=[18,28,8];cube(box,true);

=== sphere ===
----
Creates a sphere at the origin of the coordinate system. The r argument name is optional. To use d instead of r, d must be named.

Parameters

; r : Radius.  This is the radius of the sphere.  The resolution of the sphere is based on the size of the sphere and the $fa, $fs and $fn variables. For more information on these special variables look at: [[OpenSCAD_User_Manual/Other_Language_Features]]
; d : Diameter.  This is the diameter of the sphere.
; $fa : Fragment angle in degrees
; $fs : Fragment size in mm
; $fn : Resolution
  default values:  sphere();   yields:   sphere($fn = 0, $fa = 12, $fs = 2, r = 1);

Usage Examples
 sphere(r = 1);
 sphere(r = 5);
 sphere(r = 10);
 sphere(d = 2);
 sphere(d = 10);
 sphere(d = 20);

 // this creates a high resolution sphere with a 2mm radius
 sphere(2, $fn=100); 

 // also creates a 2mm high resolution sphere but this one 
 // does not have as many small triangles on the poles of the sphere
 sphere(2, $fa=5, $fs=0.1); 

[[File:OpenSCAD sphere in different sizes.png|Sample OpenSCAD spheres, showing clearly the difference in scale.]]

=== cylinder ===
----
Creates a cylinder or cone centered about the z axis. When center is true, it is also centered vertically along the z axis.

Parameter names are optional if given in the order shown here. If a parameter is named, all following parameters must also be named.

 cylinder(h = height, r1 = BottomRadius, r2 = TopRadius, center = true/false);

NOTES: 

The 2nd & 3rd positional parameters are r1 & r2, if r, d, d1 or d2 are used they must be named.

Using r1 & r2 or d1 & d2 with either value of zero will make a cone shape, a non-zero non-equal value will produce a section of a cone (a [[w:Frustum|Conical Frustum]]). r1 & d1 define the base width, at [0,0,0], and r2 & d2 define the top width.

:Parameters

:: h : height of the cylinder or cone
:: r  : radius of cylinder. r1 = r2 = r.
:: r1 : radius, bottom of cone.
:: r2 : radius, top of cone.
:: d  : diameter of cylinder. r1 = r2 = d / 2. {{requires|2014.03}}
:: d1 : diameter, bottom of cone. r1 = d1 / 2. {{requires|2014.03}}
:: d2 : diameter, top of cone. r2 = d2 / 2. {{requires|2014.03}}
::  center
::: false (default), z ranges from 0 to h
::: true,  z ranges from -h/2 to +h/2
:: $fa : minimum angle (in degrees) of each fragment.
:: $fs : minimum circumferential length of each fragment.
:: $fn : fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs
:::$fa, $fs and $fn must be named parameters. [[OpenSCAD_User_Manual/Other_Language_Features|click here for more details,]].

 defaults: cylinder();  yields: cylinder($fn = 0, $fa = 12, $fs = 2, h = 1, r1 = 1, r2 = 1, center = false);

[[File:OpenSCAD Cone 15x10x20.jpg|200px]]
 equivalent scripts
  cylinder(h=15, r1=9.5, r2=19.5, center=false);
  cylinder(  15,    9.5,    19.5, false);
  cylinder(  15,    9.5,    19.5);
  cylinder(  15,    9.5, d2=39  );
  cylinder(  15, d1=19,  d2=39  );
  cylinder(  15, d1=19,  r2=19.5);

[[File:OpenSCAD Cone 15x10x0.jpg|200px]]
 equivalent scripts
  cylinder(h=15, r1=10, r2=0, center=true);
  cylinder(  15,    10,    0,        true);
  cylinder(h=15, d1=20, d2=0, center=true);

<gallery>
image:OpenSCAD Cylinder 20x10 false.jpg|center = false
File:OpenSCAD Cylinder 20x10 true.jpg|center = true
</gallery>
 equivalent scripts
  cylinder(h=20, r=10, center=true);
  cylinder(  20,   10, 10,true);
  cylinder(  20, d=20, center=true);
  cylinder(  20,r1=10, d2=20, center=true);
  cylinder(  20,r1=10, d2=2*10, center=true);

:use of $fn
Larger values of $fn create smoother, more circular, surfaces at the cost of longer rendering time. Some use medium values during development for the faster rendering, then change to a larger value for the final F6 rendering. 

However, use of small values can produce some interesting non circular objects. A few examples are show here:
<gallery>
 File:3 sided fiqure.jpg 
 File:4 sided pyramid.jpg 
 File:4 sided part pyramid.jpg 
</gallery>
 scripts for these examples
  cylinder(20,20,20,$fn=3);
  cylinder(20,20,00,$fn=4);
  cylinder(20,20,10,$fn=4);

:undersized holes
Using cylinder() with difference() to place holes in objects creates undersized holes. This is because circular paths are approximated with polygons inscribed within in a circle. The points of the polygon are on the circle, but straight lines between are inside. To have all of the hole larger than the true circle, the polygon must lie wholly outside of the circle (circumscribed). [[OpenSCAD User Manual/undersized circular objects|Modules for circumscribed holes]]

<gallery>
 File:OpenSCAD Under size hole.jpg
</gallery>
 script for this example
  poly_n = 6;
  color("blue") translate([0, 0, 0.02]) linear_extrude(0.1) circle(10, $fn=poly_n);
  color("green") translate([0, 0, 0.01]) linear_extrude(0.1) circle(10, $fn=360);
  color("purple") linear_extrude(0.1) circle(10/cos(180/poly_n), $fn=poly_n);

In general, a polygon of radius <math>r</math> has a radius to the midpoint of any side as <math>r_m = r \cos(180/n)</math>. If only the midpoint radius <math>r_m</math> is known (for example, to fit a hex key into a hexagonal hole), then the polygon radius is <math>r = \frac{r_m}{\cos(180/n)}</math>.

=== polyhedron ===
----
A polyhedron is the most general 3D primitive solid. It can be used to create any regular or irregular shape including those with concave as well as convex features. Curved surfaces are approximated by a series of flat surfaces.

 polyhedron( points = [ [X<sub>0</sub>, Y<sub>0</sub>, Z<sub>0</sub>], [X<sub>1</sub>, Y<sub>1</sub>, Z<sub>1</sub>], ... ], triangles = [ [P<sub>0</sub>, P<sub>1</sub>, P<sub>2</sub>], ... ], convexity = N);   // before 2014.03
 polyhedron( points = [ [X<sub>0</sub>, Y<sub>0</sub>, Z<sub>0</sub>], [X<sub>1</sub>, Y<sub>1</sub>, Z<sub>1</sub>], ... ], faces = [ [P<sub>0</sub>, P<sub>1</sub>, P<sub>2</sub>, P<sub>3</sub>, ...], ... ], convexity = N);   // 2014.03 & later

:Parameters
:: points 
::: Vector of 3d points or vertices. Each point is in turn a vector, [x,y,z], of its coordinates. 
::: Points may be defined in any order. N points are referenced, in the order defined, as 0 to N-1.

:: triangles {{OpenSCAD_User_Manual/Deprecated|triangles|Use faces parameter instead}}
:::  Vector of faces that collectively enclose the solid. Each face is a vector containing the indices (0 based) of 3 points from the points vector.

:: faces {{requires|2014.03}}
:::  Vector of faces that collectively enclose the solid. Each face is a vector containing the indices (0 based) of 3 or more points from the points vector.
::: Faces may be defined in any order, but the points of each face must be ordered correctly (see below). Define enough faces to fully enclose the solid, with no overlap.
::: If points that describe a single face are not on the same plane, the face is automatically split into triangles as needed. 

:: convexity
::: Integer. The convexity parameter specifies the maximum number of faces a ray intersecting the object might penetrate. This parameter is needed only for correct display of the object in OpenCSG preview mode. It has no effect on the polyhedron rendering. For display problems, setting it to 10 should work fine for most cases.

  default values: polyhedron(); yields: polyhedron(points = undef, faces = undef, convexity = 1);

In the list of faces, for each face it is arbitrary which point you start with, but the points of the face (referenced by the index into the list of points) must be ordered in clockwise direction when looking at each face from outside inward. The back is viewed from the back, the bottom from the bottom, etc.

Another way to remember this ordering requirement is to use the left-hand rule. Using your left hand, stick your thumb up and curl your fingers as if giving the thumbs-up sign, point your thumb away from the face, and order the points in the direction your fingers curl (this is the opposite of the [[w:STL (file format)#Facet normal|STL file format]] convention, which uses a "right-hand rule"). Try this on the example below.

:Example 1 Using polyhedron to generate cube( [ 10, 7, 5 ] ); 
[[File:Cube_numbers.jpg|frame|left|point numbers for cube]]
[[File:Cube_flat.jpg|frame|center|unfolded cube faces]] 
 <br>
 CubePoints = [
   [  0,  0,  0 ],  //0
   [ 10,  0,  0 ],  //1
   [ 10,  7,  0 ],  //2
   [  0,  7,  0 ],  //3
   [  0,  0,  5 ],  //4
   [ 10,  0,  5 ],  //5
   [ 10,  7,  5 ],  //6
   [  0,  7,  5 ]]; //7

 CubeFaces = [
   [0,1,2,3],  // bottom
   [4,5,1,0],  // front
   [7,6,5,4],  // top
   [5,6,2,1],  // right
   [6,7,3,2],  // back
   [7,4,0,3]]; // left

 polyhedron( CubePoints, CubeFaces );

 equivalent descriptions of the bottom face
   [0,1,2,3],
   [0,1,2,3,0],
   [1,2,3,0],
   [2,3,0,1],
   [3,0,1,2],
   [0,1,2],[2,3,0],   // 2 triangles with no overlap
   [1,2,3],[3,0,1],
   [1,2,3],[0,1,3],
:Example 2  A square base pyramid:

[[File:Openscad-polyhedron-squarebasepyramid.png|frame|none|A simple polyhedron, square base pyramid]]
 polyhedron(
   points=[ [10,10,0],[10,-10,0],[-10,-10,0],[-10,10,0], // the four points at base
            [0,0,10]  ],                                 // the apex point 
   faces=[ [0,1,4],[1,2,4],[2,3,4],[3,0,4],              // each triangle side
               [1,0,3],[2,1,3] ]                         // two triangles for square base
  );
:Example 3  A triangular prism:

Note: There is an error in this example, a ''steely-eyed CAD Man'' noticed the unfolded triangles are incorrect, the hypotenuse should be 1,5 & 0,4.
The correct unfold is to have them next to rectangle A, along sides 1,2 & 0,3. The code has been corrected, hopefully a revised image will arrive in due course.
<br>

[[File:Polyhedron Prism.png|thumb|none|600px|A polyhedron triangular prism]]
   module prism(l, w, h){
       polyhedron(//pt 0        1        2        3        4        5
               points=[[0,0,0], [l,0,0], [l,w,0], [0,w,0], [0,w,h], [l,w,h]],
               faces=[[0,1,2,3],[5,4,3,2],[0,4,5,1],[0,3,4],[5,2,1]]
               );

       // preview unfolded (do not include in your function
       z = 0.08;
       separation = 2;
       border = .2;
       translate([0,w+separation,0])
           cube([l,w,z]);
       translate([0,w+separation+w+border,0])
           cube([l,h,z]);
       translate([0,w+separation+w+border+h+border,0])
           cube([l,sqrt(w*w+h*h),z]);
       translate([l+border,w+separation,0])
           polyhedron(//pt 0       1       2        3       4       5
                   points=[[0,0,0],[h,w,0],[0,w,0], [0,0,z],[h,w,z],[0,w,z]],
                   faces=[[0,1,2], [3,5,4], [0,3,4,1], [1,4,5,2], [2,5,3,0]]
                   );
       translate([0-border,w+separation,0])
           polyhedron(//pt 0       1         2        3       4         5
                   points=[[0,0,0],[0-h,w,0],[0,w,0], [0,0,z],[0-h,w,z],[0,w,z]],
                   faces=[[1,0,2],[5,3,4],[0,1,4,3],[1,2,5,4],[2,0,3,5]]
                   );
       }

   prism(10, 5, 3);
==== Debugging polyhedra ====
----
Mistakes in defining polyhedra include not having all faces in clockwise order (viewed from outside - a bottom need to be viewed from below), overlap of faces and missing faces or portions of faces. As a general rule, the polyhedron faces should also satisfy manifold conditions:
* exactly two faces should meet at any polyhedron edge.
* if two faces have a vertex in common, they should be in the same cycle face-edge around the vertex.
The first rule eliminates polyhedra like two cubes with a common edge and not watertight models; the second excludes polyhedra like two cubes with a common vertex.

When viewed from the outside, the points describing each face must be in the same clockwise order, and provides a mechanism for detecting counterclockwise.
When the thrown together view (F12) is used with F5, CCW faces are shown in pink. Reorder the points for incorrect faces. Rotate the object to view all faces. The pink view can be turned off with F10.

OpenSCAD allows, temporarily, commenting out part of the face descriptions so that only the remaining faces are displayed. Use // to comment out the rest of the line. Use /* and */ to start and end a comment block. This can be part of a line or extend over several lines. Viewing only part of the faces can be helpful in determining the right points for an individual face. Note that a solid is not shown, only the faces. If using F12, all faces have one pink side. Commenting some faces helps also to show any internal face.


[[File:Cube_2_face.jpg|frame|left|example 1 showing only 2 faces]]

 CubeFaces = [
 /* [0,1,2,3],  // bottom
    [4,5,1,0],  // front */
    [7,6,5,4],  // top
 /* [5,6,2,1],  // right
    [6,7,3,2],  // back */
    [7,4,0,3]]; // left
<br clear="all">

After defining a polyhedron, its preview may seem correct. The polyhedron alone may even render fine. However, to be sure it is a valid manifold and that it can generate a valid STL file, union it with any cube and render it (F6). If the polyhedron disappears, it means that it is not correct. Revise the winding order of all faces and the two rules stated above.

==== Mis-ordered faces ====
----
:Example 4 a more complex polyhedron with mis-ordered faces
When you select 'Thrown together' from the view menu and compile (preview F5) the design
(not compile and render!) the preview shows the mis-oriented polygons highlighted. Unfortunately this highlighting is not possible in the OpenCSG preview mode because it would interfere with the way the OpenCSG preview mode is implemented.)

Below you can see the code and the picture of such a problematic polyhedron, the bad polygons (faces or compositions of faces) are in pink.
<syntaxhighlight lang="java">
// Bad polyhedron
polyhedron
    (points = [
	       [0, -10, 60], [0, 10, 60], [0, 10, 0], [0, -10, 0], [60, -10, 60], [60, 10, 60], 
	       [10, -10, 50], [10, 10, 50], [10, 10, 30], [10, -10, 30], [30, -10, 50], [30, 10, 50]
	       ], 
     faces = [
		  [0,2,3],   [0,1,2],  [0,4,5],  [0,5,1],   [5,4,2],  [2,4,3],
                  [6,8,9],  [6,7,8],  [6,10,11], [6,11,7], [10,8,11],
		  [10,9,8], [0,3,9],  [9,0,6], [10,6, 0],  [0,4,10],
                  [3,9,10], [3,10,4], [1,7,11],  [1,11,5], [1,7,8],  
                  [1,8,2],  [2,8,11], [2,11,5]
		  ]
     );
</syntaxhighlight>
[[image:openscad-bad-polyhedron.png|frame|none|Polyhedron with badly oriented polygons]]

A correct polyhedron would be the following:
<syntaxhighlight lang="java">
polyhedron
    (points = [
	       [0, -10, 60], [0, 10, 60], [0, 10, 0], [0, -10, 0], [60, -10, 60], [60, 10, 60], 
	       [10, -10, 50], [10, 10, 50], [10, 10, 30], [10, -10, 30], [30, -10, 50], [30, 10, 50]
	       ], 
     faces = [
		  [0,3,2],  [0,2,1],  [4,0,5],  [5,0,1],  [5,2,4],  [4,2,3],
                  [6,8,9],  [6,7,8],  [6,10,11],[6,11,7], [10,8,11],
		  [10,9,8], [3,0,9],  [9,0,6],  [10,6, 0],[0,4,10],
                  [3,9,10], [3,10,4], [1,7,11], [1,11,5], [1,8,7],  
                  [2,8,1],  [8,2,11], [5,11,2]
		  ]
     );
</syntaxhighlight>

;Beginner's tip

If you don't really understand "orientation", try to identify the mis-oriented pink faces and then invert the sequence of the references to the points vectors until you get it right. E.g. in the above example, the third triangle (''[0,4,5]'') was wrong and we fixed it as ''[4,0,5]''. Remember that a face list is a circular list. In addition, you may select "Show Edges" from the "View Menu", print a screen capture and number both the points and the faces.  In our example, the points are annotated in black and the faces in blue. Turn the object around and make a second copy from the back if needed. This way you can keep track.

;Clockwise technique

Orientation is determined by clockwise circular indexing. This means that if you're looking at the triangle (in this case [4,0,5]) from the outside you'll see that the path is clockwise around the center of the face. The winding order [4,0,5] is clockwise and therefore good.  The winding order [0,4,5] is counter-clockwise and therefore bad. Likewise, any other clockwise order of [4,0,5] works: [5,4,0] & [0,5,4] are good too. If you use the clockwise technique, you'll always have your faces outside (outside of OpenSCAD, other programs do use counter-clockwise as the outside though).

Think of it as a "left hand rule":

If you place your left hand on the face with your fingers curled in the direction of the order of the points, your thumb should point outward. If your thumb points inward, you need to reverse the winding order.

[[image:openscad-bad-polyhedron-annotated.png|frame|none|Polyhedron with badly oriented polygons]]

Succinct description of a 'Polyhedron'

* Points define all of the points/vertices in the shape.
* Faces is a list of polygons that connect up the points/vertices. 

Each point, in the point list, is defined with a 3-tuple x,y,z position specification. Points in the point list are automatically enumerated starting from zero for use in the faces list (0,1,2,3,... etc).

Each face, in the faces list, is defined by selecting 3 or more of the points (using the point order number) out of the point list.

e.g. faces=[ [0,1,2] ] defines a triangle from the first point (points are zero referenced) to the second point and then to the third point.

When looking at any face from the outside, the face must list all points in a clockwise order.

==== Point repetitions in a polyhedron point list ====
The point list of the polyhedron definition may have repetitions. When two or more points have the same coordinates they are considered the same polyhedron vertex. So, the following polyhedron:

<syntaxhighlight lang="javascript">
points = [[ 0, 0, 0], [10, 0, 0], [ 0,10, 0],
          [ 0, 0, 0], [10, 0, 0], [ 0,10, 0],
          [ 0,10, 0], [10, 0, 0], [ 0, 0,10],
          [ 0, 0, 0], [ 0, 0,10], [10, 0, 0],
          [ 0, 0, 0], [ 0,10, 0], [ 0, 0,10]];
polyhedron(points, [[0,1,2], [3,4,5], [6,7,8], [9,10,11], [12,13,14]]);
</syntaxhighlight>

define the same tetrahedron as:

<syntaxhighlight lang="javascript">
points = [[0,0,0], [0,10,0], [10,0,0], [0,0,10]];
polyhedron(points, [[0,2,1], [0,1,3], [1,2,3], [0,3,2]]);
</syntaxhighlight>

{{BookCat}}

[[it:OpenSCAD/Primitive_solidi]]
[[ru:Руководство_пользователя_по_OpenSCAD/Примитивы_объемных_тел]]

=== boolean overview ===
===== 2D examples =====
<gallery >
File:OpenSCAD Boolean Union 2D.jpg|        union ( or )           <br/> circle + square 
File:OpenSCAD Boolean Difference 2D.jpg|   difference ( and not ) <br/> square - circle
File:OpenSCAD Boolean Difference 1 2D.jpg| difference ( and not ) <br/> circle - square
File:OpenSCAD Boolean Intersection 2D.jpg| intersection ( and )   <br/> circle - (circle - square)
</gallery>
<syntaxhighlight lang="javascript">
 union()       {square(10);circle(10);} // square or  circle
 difference()  {square(10);circle(10);} // square and not circle
 difference()  {circle(10);square(10);} // circle and not square
 intersection(){square(10);circle(10);} // square and circle
</syntaxhighlight>
===== 3D examples =====
<gallery >
File:OpenScad Boolean Union.jpg|        union ( or )           <br/> sphere + cube 
File:Boolean Difference 1a.jpg|         difference ( and not ) <br/> cube - sphere
File:OpenScad Boolean Difference 2.jpg| difference ( and not ) <br/> sphere - cube
File:OpenScad Boolean Intersection.jpg| intersection ( and )   <br/> sphere - (sphere - cube)
</gallery>
<syntaxhighlight lang="javascript">
 union()       {cube(12, center=true); sphere(8);} // cube or  sphere
 difference()  {cube(12, center=true); sphere(8);} // cube and not sphere
 difference()  {sphere(8); cube(12, center=true);} // sphere and not cube
 intersection(){cube(12, center=true); sphere(8);} // cube and sphere
</syntaxhighlight>
=== union ===

Creates a union of all its child nodes. This is the sum of all children (logical or).<br />
May be used with either 2D or 3D objects, but don't mix them.

[[Image:Openscad_union.jpg|400px|Union]]
<syntaxhighlight lang="javascript">
 //Usage example:
 union() {
 	cylinder (h = 4, r=1, center = true, $fn=100);
 	rotate ([90,0,0]) cylinder (h = 4, r=0.9, center = true, $fn=100);
 }
</syntaxhighlight>
Remark: union is implicit when not used. But it is mandatory, for example, in difference to group first child nodes into one.

<b>Note:</b> It is mandatory for all unions, explicit or implicit, that external faces to be merged not be coincident.  Failure to follow this rule results in a design with undefined behavior, and can result in a render which is not manifold (with zero volume portions, or portions inside out), which typically leads to a warning and sometimes removal of a portion of the design from the rendered output.  (This can also result in [[OpenSCAD_User_Manual/FAQ#What_are_those_strange_flickering_artifacts_in_the_preview?|flickering effects during the preview]].)  This requirement is not a bug, but an intrinsic property of floating point comparisons and the fundamental inability to exactly represent irrational numbers such as those resulting from most rotations.  As an example, this is an invalid OpenSCAD program, and will at least lead to a warning on most platforms:

<syntaxhighlight lang="javascript">
 // Invalid!
 size = 10;
 rotation = 17;
 union() {
    rotate([rotation, 0, 0])
       cube(size);
    rotate([rotation, 0, 0])
       translate([0, 0, size])
       cube([2, 3, 4]);
 }
</syntaxhighlight>

The solution is to always use a small value called an epsilon when merging adjacent faces like this to guarantee overlap.  Note the 0.01 eps value used in TWO locations, so that the external result is equivalent to what was intended:

<syntaxhighlight lang="javascript">
 // Correct!
 size = 10;
 rotation = 17;
 eps = 0.01;
 union() {
    rotate([rotation, 0, 0])
       cube(size);
    rotate([rotation, 0, 0])
       translate([0, 0, size-eps])
       cube([2, 3, 4+eps]);
 }
</syntaxhighlight>

=== difference ===

Subtracts the 2nd (and all further) child nodes from the first one (logical and not).<br />
May be used with either 2D or 3D objects, but don't mix them.

[[Image:Openscad_difference.jpg|400px|Difference]]
<syntaxhighlight lang="javascript">
Usage example:
difference() {
	cylinder (h = 4, r=1, center = true, $fn=100);
	rotate ([90,0,0]) cylinder (h = 4, r=0.9, center = true, $fn=100);
}
</syntaxhighlight>

<b>Note:</b> It is mandatory that surfaces that are to be removed by a difference operation have an overlap, and that the negative piece being removed extends fully outside of the volume it is removing that surface from.  Failure to follow this rule can cause [[OpenSCAD_User_Manual/FAQ#What_are_those_strange_flickering_artifacts_in_the_preview?|preview artifacts]] and can result in non-manifold render warnings or the removal of pieces from the render output.  See the description above in union for why this is required and an example of how to do this by this using a small epsilon value.

===== difference with multiple children =====
Note, in the second instance, the result of adding a union of the 1st and 2nd children.

[[File:Bollean Difference 3.jpg|300px]]
<syntaxhighlight lang="javascript">
// Usage example for difference of multiple children:
$fn=90;
difference(){
                                            cylinder(r=5,h=20,center=true);
    rotate([00,140,-45]) color("LightBlue") cylinder(r=2,h=25,center=true);
    rotate([00,40,-50])                     cylinder(r=2,h=30,center=true);
    translate([0,0,-10])rotate([00,40,-50]) cylinder(r=1.4,h=30,center=true);
}

// second instance with added union
translate([10,10,0]){
    difference(){
      union(){        // combine 1st and 2nd children
                                                cylinder(r=5,h=20,center=true);
        rotate([00,140,-45]) color("LightBlue") cylinder(r=2,h=25,center=true);
      }
      rotate([00,40,-50])                       cylinder(r=2,h=30,center=true);
      translate([0,0,-10])rotate([00,40,-50])   cylinder(r=1.4,h=30,center=true);
    }
}
</syntaxhighlight>

=== intersection ===

Creates the intersection of all child nodes. This keeps the overlapping portion (logical and).
<br />
Only the area which is common or shared by all children is retained.<br />
May be used with either 2D or 3D objects, but don't mix them.

[[Image:Openscad_intersection.jpg|400px|Intersection]]
<syntaxhighlight lang="javascript">
//Usage example:
intersection() {
	cylinder (h = 4, r=1, center = true, $fn=100);
	rotate ([90,0,0]) cylinder (h = 4, r=0.9, center = true, $fn=100);
}
</syntaxhighlight>


=== render ===


<syntaxhighlight lang="javascript">
Usage example:
render(convexity = 1) { ... }
</syntaxhighlight>

{| border=1
|-
|convexity
|Integer. The convexity parameter specifies the maximum number of front and back sides a ray intersecting the object might penetrate. This parameter is only needed for correctly displaying the object in OpenCSG preview mode and has no effect on the polyhedron rendering.
|}


[[Image:Openscad_convexity.jpg|400px|]]

This image shows a 2D shape with a convexity of 4, as the ray indicated in red crosses the 2D shape a maximum of 4 times. The convexity of a 3D shape would be determined in a similar way. Setting it to 10 should work fine for most cases.

{{BookCat}}
'''


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_openscad(huit_api_key, processed_image_path):
    """
    Send processed image data to HUIT proxy to get JSON interpretation.
    """
    # Define the HUIT proxy endpoint
    url = "https://go.apis.huit.harvard.edu/ais-openai-direct/v1/chat/completions"

    # Prepare the headers
    headers = {
        "api-key": huit_api_key,
        "Content-Type": "application/json"
    }

    base64_image = encode_image(processed_image_path)

    # Prepare the data payload
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": OPENSCAD_DOCS},
            {"role": "user", "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Describe the shape in this image using the OpenSCAD language. Return only the code, with no other text before or after. Use boolean operations to construct the shape out of primitive shapes. Keep in mind it may require many boolean operations. Start from the biggest shape and work your way in."
                    },
                ],
             }
        ]
    }

    # Make the POST request to the HUIT proxy
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        output_json = response.json()
        output_path = "output/drawing_output.json"
        with open(output_path, "w") as file:
            json.dump(output_json, file, indent=4)
        print(f"JSON output saved at: {output_path}")
        print(output_json["choices"][0]["message"]["content"])
        return output_json
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    huit_api_key = "gb8bqMD0wrPkM040h1dvOz6LTEIZCa5y"  # Replace with your HUIT API key
    processed_image_path = "input/isometric_drawing.png"
    generate_openscad(huit_api_key, processed_image_path)


