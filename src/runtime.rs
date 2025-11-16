use crate::display::MockDisplay;
use firefly_runtime::{Rgb16, Runtime};
use std::sync::Mutex;

type RealRuntime<'a> = Runtime<'a, MockDisplay, Rgb16>;

/// A global Runtime instance.
///
/// We have to store the Runtime globally to have 'static runtime for it.
static mut RUNTIME: Mutex<Option<MockRuntime>> = Mutex::new(None);

pub fn set_runtime(runtime: RealRuntime<'static>) -> Result<(), &'static str> {
    unsafe {
        let runtime = MockRuntime::new(runtime);
        #[allow(static_mut_refs)]
        let Ok(mut cell) = RUNTIME.lock() else {
            return Err("lock is poisoned");
        };
        cell.replace(runtime);
        Ok(())
    }
}

pub fn get_runtime<'a>() -> Result<&'a mut RealRuntime<'static>, &'static str> {
    unsafe {
        #[allow(static_mut_refs)]
        let Ok(runtime) = RUNTIME.get_mut() else {
            return Err("lock is poisoned");
        };
        let Some(runtime) = runtime.as_mut() else {
            return Err("runtime is not initialized");
        };
        Ok(&mut runtime.runtime)
    }
}

/// An unsafe wrapper for Runtime implementing Send and Sync.
///
/// Required for storing Runtime in a global static.
pub struct MockRuntime<'a> {
    runtime: RealRuntime<'a>,
}

impl<'a> MockRuntime<'a> {
    pub fn new(runtime: RealRuntime<'a>) -> Self {
        Self { runtime }
    }
}

unsafe impl<'a> Send for MockRuntime<'a> {}
unsafe impl<'a> Sync for MockRuntime<'a> {}
