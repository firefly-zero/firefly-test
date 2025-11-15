mod color;
mod display;
mod runner;
mod runtime;
use pyo3::prelude::*;

/// Framework for testing Firefly Zero games.
#[pymodule]
#[pyo3(name = "_rust")]
fn firefly_test(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<runner::Runner>()?;
    m.add_class::<color::Color>()?;
    Ok(())
}
