// Dimensions
cube_size = 10;  // Size of each cube
gap_size = 2;    // Gap between parts (adjust as needed)

// Base block
difference() {
    cube([3 * cube_size, 2 * cube_size, cube_size]);
    translate([2 * cube_size, cube_size, 0])
        cube([cube_size, cube_size, cube_size]);
}

// Upper block
translate([2 * cube_size, cube_size, cube_size])
    cube([cube_size, cube_size, cube_size]);


Claude 

// L-shaped 3D model
// All dimensions are in millimeters

// Base block dimensions
base_length = 60;
base_width = 40;
base_height = 20;

// Top block dimensions
top_length = 30;
top_width = 20;
top_height = 20;

// Create the base block
cube([base_length, base_width, base_height]);

// Create the top block
// Positioned to create an L-shape
translate([base_length - top_length, 0, base_height])
    cube([top_length, top_width, top_height]);