use crate::display::MockDisplay;
use directories::ProjectDirs;
use embedded_graphics::pixelcolor::Rgb888;
use firefly_hal::*;
use firefly_runtime::*;
use pyo3::exceptions::{PyRuntimeError, PyTypeError};
use pyo3::prelude::*;
use std::path::PathBuf;

#[pyclass(unsendable)]
pub struct Runner {
    runtime: Box<Runtime<MockDisplay, Rgb888>>,
}

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
        let Ok(author_id) = heapless::String::<16>::try_from(author_id.as_str()) else {
            return Err(PyTypeError::new_err("invalid author_id"));
        };
        let Ok(app_id) = heapless::String::<16>::try_from(app_id.as_str()) else {
            return Err(PyTypeError::new_err("invalid app_id"));
        };
        let id = FullID::new(author_id, app_id);
        let display = MockDisplay::new();
        let config = RuntimeConfig {
            id: Some(id),
            device,
            display,
            net_handler: NetHandler::None,
        };
        let runtime = match Runtime::new(config) {
            Ok(runtime) => runtime,
            Err(err) => return Err(PyRuntimeError::new_err(err.to_string())),
        };
        let runner = Self {
            runtime: Box::new(runtime),
        };
        Ok(runner)
    }

    fn start(&mut self) -> PyResult<()> {
        match self.runtime.start() {
            Ok(()) => Ok(()),
            Err(err) => Err(PyRuntimeError::new_err(err.to_string())),
        }
    }

    fn update(&mut self) -> PyResult<bool> {
        match self.runtime.update() {
            Ok(exit) => Ok(exit),
            Err(err) => Err(PyRuntimeError::new_err(err.to_string())),
        }
    }

    fn get_frame(&mut self) -> Vec<u32> {
        self.runtime.display().buf.into()
    }

    fn set_input(&mut self, x: i16, y: i16, b: u8) {
        let pad = if x == 0xFF && y == 0xFF {
            Some(Pad { x, y })
        } else {
            None
        };
        let input = InputState { pad, buttons: b };
        self.runtime.device_mut().update_input(input)
    }
}

/// Get path to the virtual file system.
fn get_vfs_path() -> PathBuf {
    match ProjectDirs::from("com", "firefly", "firefly") {
        Some(dirs) => dirs.data_dir().to_owned(),
        None => PathBuf::from(".firefly"),
    }
}
