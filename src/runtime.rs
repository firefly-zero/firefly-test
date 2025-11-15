use crate::display::MockDisplay;
use core::mem::MaybeUninit;
use firefly_runtime::{Rgb16, Runtime};
use std::sync::Mutex;

type RealRuntime<'a> = Runtime<'a, MockDisplay, Rgb16>;

/// A global Runtime instance.
///
/// We have to store the Runtime globally to have 'static runtime for it.
static mut RUNTIME: Mutex<MaybeUninit<MockRuntime>> = Mutex::new(MaybeUninit::uninit());

pub fn set_runtime(runtime: RealRuntime<'static>) {
    unsafe {
        let runtime = MockRuntime::new(runtime);
        let mut cell = RUNTIME.lock().unwrap();
        cell.assume_init_drop();
        cell.write(runtime);
    }
}

pub fn get_runtime<'a>() -> &'a mut RealRuntime<'static> {
    unsafe {
        let runtime = RUNTIME.get_mut().unwrap();
        let runtime = runtime.assume_init_mut();
        &mut runtime.runtime
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
