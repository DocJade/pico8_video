// DocJade.

#![warn(
    clippy::pedantic,
    clippy::nursery,
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::correctness,
    clippy::style,
    clippy::perf
)]

// import the modules.
mod image_actions;

// I like my clippy to be paranoid.


// TODO:
//
// Separate the video that was input into its frames (image_actions)
// 

const PICO_COLORS: [(&str, u8, u8, u8); 16] = [
    //ID,  R, G, B
    ("00", 0, 0, 0),       //black
    ("01", 29, 43, 83),    //dark-blue
    ("02", 126, 37, 83),   //dark-purple
    ("03", 0, 135, 81),    //dark-green
    ("04", 171, 82, 54),   //brown
    ("05", 95, 87, 79),    //dark-grey
    ("06", 194, 195, 199), //light-grey
    ("07", 255, 241, 232), //white
    ("08", 255, 0, 77),    //red
    ("09", 255, 163, 0),   //orange
    ("10", 255, 236, 39),  //yellow
    ("11", 0, 228, 54),    //green
    ("12", 41, 173, 255),  //blue
    ("13", 131, 118, 156), //lavender
    ("14", 255, 119, 168), //pink
    ("15", 255, 204, 170), //light-peach
];

fn main() {
    println!("Hello, world!");
}
