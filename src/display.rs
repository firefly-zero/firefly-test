use embedded_graphics::pixelcolor::Rgb888;
use embedded_graphics::prelude::{Dimensions, DrawTarget, OriginDimensions, Point, Size};
use embedded_graphics::primitives::Rectangle;
use firefly_runtime::{HEIGHT, WIDTH};
use std::convert::Infallible;
const BUF_SIZE: usize = WIDTH * HEIGHT;

pub(crate) struct MockDisplay {
    buf: [Rgb888; BUF_SIZE],
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
        I: IntoIterator<Item = embedded_graphics::Pixel<Self::Color>>,
    {
        todo!()
    }
}
