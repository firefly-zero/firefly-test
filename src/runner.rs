use crate::display::MockDisplay;
use crate::runtime::{get_runtime, set_runtime};
use directories::ProjectDirs;
use firefly_hal::*;
use firefly_runtime::*;
use pyo3::exceptions::{PyRuntimeError, PyTypeError};
use pyo3::prelude::*;
use std::path::PathBuf;

#[pyclass(unsendable)]
pub struct Runner {}

#[pymethods]
impl Runner {
    #[new]
    fn new(author_id: String, app_id: String, vfs_path: String) -> PyResult<Self> {
        let vfs_path: PathBuf = if vfs_path.is_empty() {
            get_vfs_path()
        } else {
            vfs_path.into()
        };
        let config = DeviceConfig {
            root: vfs_path,
            ..Default::default()
        };
        let device = DeviceImpl::new(config);
        let Some(id) = FullID::from_str(author_id.as_str(), app_id.as_str()) else {
            return Err(PyTypeError::new_err("invalid author/app ID"));
        };
        let display = MockDisplay::new();
        let config = RuntimeConfig {
            id: Some(id),
            device,
            display,
            net_handler: NetHandler::None,
        };
        let runtime = match Runtime::new(config) {
            Ok(runtime) => runtime,
            Err(err) => make_error(&err.to_string())?,
        };

        let res = set_runtime(runtime);
        if let Err(err) = res {
            make_error(err)?;
        }
        Ok(Self {})
    }

    fn start(&mut self) -> PyResult<()> {
        let runtime = match get_runtime() {
            Ok(runtime) => runtime,
            Err(err) => make_error(err)?,
        };
        match runtime.start() {
            Ok(()) => Ok(()),
            Err(err) => Err(PyRuntimeError::new_err(err.to_string())),
        }
    }

    fn update(&mut self) -> PyResult<bool> {
        let runtime = match get_runtime() {
            Ok(runtime) => runtime,
            Err(err) => make_error(err)?,
        };
        runtime.set_render_every(1);
        match runtime.update() {
            Ok(exit) => Ok(exit),
            Err(err) => Err(PyRuntimeError::new_err(err.to_string())),
        }
    }

    fn get_frame(&mut self) -> PyResult<Vec<u16>> {
        let runtime = match get_runtime() {
            Ok(runtime) => runtime,
            Err(err) => make_error(err)?,
        };
        Ok(runtime.display_mut().buf.into())
    }

    fn set_input(&mut self, x: i16, y: i16, b: u8) -> PyResult<()> {
        let pad = if x == 0xFF && y == 0xFF {
            Some(Pad { x, y })
        } else {
            None
        };
        let input = InputState { pad, buttons: b };
        let runtime = match get_runtime() {
            Ok(runtime) => runtime,
            Err(err) => make_error(err)?,
        };
        runtime.device_mut().update_input(input);
        Ok(())
    }
}

/// Get path to the virtual file system.
fn get_vfs_path() -> PathBuf {
    match ProjectDirs::from("com", "firefly", "firefly") {
        Some(dirs) => dirs.data_dir().to_owned(),
        None => PathBuf::from(".firefly"),
    }
}

fn make_error<T>(err: &'_ str) -> PyResult<T> {
    Err(PyRuntimeError::new_err(err.to_string()))
}
