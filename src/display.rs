use embedded_graphics::pixelcolor::Rgb888;
use embedded_graphics::prelude::*;
use embedded_graphics::Pixel;
use firefly_runtime::{HEIGHT, WIDTH};
use std::convert::Infallible;

const BUF_SIZE: usize = WIDTH * HEIGHT;

pub(crate) struct MockDisplay {
    /// THe frame buffer for the display. One value is a serialized RGB value.
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
