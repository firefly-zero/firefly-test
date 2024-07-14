mod display;
mod runner;
use pyo3::prelude::*;

/// Framework for testing Firefly Zero games.
#[pymodule]
#[pyo3(name = "_rust")]
fn firefly_test(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<runner::Runner>()?;
    Ok(())
}
