use embedded_graphics::pixelcolor::Rgb888;
use embedded_graphics::prelude::*;
use embedded_graphics::primitives::Rectangle;
use embedded_graphics::Pixel;
use firefly_runtime::*;
use std::convert::Infallible;

const BUF_SIZE: usize = WIDTH * HEIGHT;

pub(crate) struct MockDisplay {
    /// The frame buffer for the display. One value is a serialized RGB value.
    pub buf: [u32; BUF_SIZE],
}

impl MockDisplay {
    pub fn new() -> Self {
        Self { buf: [0; BUF_SIZE] }
    }
}

impl OriginDimensions for MockDisplay {
    fn size(&self) -> Size {
        Size::new(WIDTH as u32, HEIGHT as u32)
    }
}

impl DrawTarget for MockDisplay {
    type Color = Rgb888;
    type Error = Infallible;

    fn draw_iter<I>(&mut self, pixels: I) -> Result<(), Self::Error>
    where
        I: IntoIterator<Item = Pixel<Self::Color>>,
    {
        for Pixel(point, color) in pixels {
            let i = point.y as usize * WIDTH + point.x as usize;
            let v = color.into_storage();
            self.buf[i] = v;
        }
        Ok(())
    }
}

impl RenderFB for MockDisplay {
    type Error = Infallible;

    fn render_fb(&mut self, frame: &mut FrameBuffer) -> Result<(), Self::Error> {
        let bbox = Rectangle::new(Point::zero(), frame.size());
        let pixels: Vec<Rgb16> = frame.iter_pairs().flat_map(|(a, b)| [a, b]).collect();
        for (point, pixel) in bbox.points().zip(pixels) {
            let i = point.y as usize * WIDTH + point.x as usize;
            let (r, g, b) = pixel.into_rgb();
            self.buf[i] = pack_rgb(r, g, b);
        }
        Ok(())
    }
}

fn pack_rgb(r: u8, g: u8, b: u8) -> u32 {
    let r = u32::from(r);
    let g = u32::from(g);
    let b = u32::from(b);
    (r << 16) | (g << 8) | b
}
