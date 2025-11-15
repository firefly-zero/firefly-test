use embedded_graphics::prelude::*;
use embedded_graphics::primitives::Rectangle;
use embedded_graphics::Pixel;
use firefly_runtime::*;
use std::convert::Infallible;

const BUF_SIZE: usize = WIDTH * HEIGHT;

pub(crate) struct MockDisplay {
    /// The frame buffer for the display. One value is a serialized RGB value.
    pub buf: [u16; BUF_SIZE],
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
    type Color = Rgb16;
    type Error = Infallible;

    fn draw_iter<I>(&mut self, pixels: I) -> Result<(), Self::Error>
    where
        I: IntoIterator<Item = Pixel<Self::Color>>,
    {
        for Pixel(point, color) in pixels {
            let i = point.y as usize * WIDTH + point.x as usize;
            self.buf[i] = (u16::from(color.0) << 8) | u16::from(color.1);
        }
        Ok(())
    }
}

impl RenderFB for MockDisplay {
    type Error = Infallible;

    fn render_fb(&mut self, frame: &mut FrameBuffer) -> Result<(), Self::Error> {
        let bbox = Rectangle::new(Point::zero(), frame.size());
        let pixels: Vec<Rgb16> = frame.iter_pairs().flat_map(|(a, b)| [a, b]).collect();
        for (point, color) in bbox.points().zip(pixels) {
            let i = point.y as usize * WIDTH + point.x as usize;
            self.buf[i] = (u16::from(color.0) << 8) | u16::from(color.1);
        }
        Ok(())
    }
}
