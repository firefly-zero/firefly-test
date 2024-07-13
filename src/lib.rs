use pyo3::prelude::*;

#[pyclass]
struct Runner {
    id: String,
}

#[pymethods]
impl Runner {
    #[new]
    fn new(id: String) -> Self {
        Runner { id }
    }
}

/// Framework for testing Firefly Zero games.
#[pymodule]
#[pyo3(name = "_rust")]
fn firefly_test(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Runner>()?;
    Ok(())
}
