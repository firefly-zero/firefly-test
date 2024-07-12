use pyo3::prelude::*;

#[pyclass]
struct Runner {
    num: i32,
}

#[pymethods]
impl Runner {
    #[new]
    fn new(num: i32) -> Self {
        Runner { num }
    }
}

/// Framework for testing Firefly Zero games.
#[pymodule]
fn firefly_test(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Runner>()?;
    Ok(())
}
