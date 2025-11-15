use firefly_runtime::Rgb16;
use pyo3::*;

#[pyclass(unsendable)]
pub struct Color {
    color: Rgb16,
}

#[pymethods]
impl Color {
    #[new]
    fn new(r: u16, g: u16, b: u16) -> PyResult<Self> {
        let color = Rgb16::from_rgb(r, g, b);
        Ok(Self { color })
    }

    #[staticmethod]
    fn from_rgb16(rgb16: u16) -> PyResult<Self> {
        let left = (rgb16 >> 8) as u8;
        let right = rgb16 as u8;
        let color = Rgb16(left, right);
        Ok(Self { color })
    }

    fn to_rgb16(&self) -> u16 {
        let color = self.color;
        (u16::from(color.0) << 8) | u16::from(color.1)
    }

    fn to_rgb(&self) -> (u8, u8, u8) {
        self.color.into_rgb()
    }
}
