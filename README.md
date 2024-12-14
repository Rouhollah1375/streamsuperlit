# StreamSuperLit

## 🚀 Introduction 🚀

Welcome to 🌟**StreamSuperLit**🌟 — a game-changer extention for your [Streamlit](https://streamlit.io/) apps! If you've ever found yourself wrestling with the chaos of unstructured Streamlit apps, and the frustration of losing object states when using [Streamlit Autorefresh](https://github.com/kmcgrady/streamlit-autorefresh) or after every user interaction, then you're in the right place! 🎯

💡 With **StreamSuperLit**, we’re taking Streamlit to the next level:
- 💼 **Bring Order to Chaos**: StreamSuperLit provides a clear, modular structure to organize your dashboard app. So, you can focus on building, not debugging. The familiar **View+Controller** structure utilized in StreamSuperLit's components is by no means limiting. Contrarily, it acts as a guideline for you to develop your app more productively.


- 🔄 **Stateful Magic**: StreamSuperLit objects (`Component`s, `View`s, and `Controller`s) stay alive and remember their state, no matter how many times your app reruns. **so, you can safely forget about dealing with `@st.cache` and its quirks!** (of course, it can still be useful sometimes)


- 🧩 **Modular and Reusable Components**: Build your app like a pro with clear separation of concerns. Also, you can easily collaborate with others on the same project without worrying about hitting conflicts!

- ⚙️ **Seamless Lifecycle Management**: Use built-in hooks to elegantly handle initializations for your components.


Thinking about compatiblity? StreamSuperLit is just an extention on the Streamlit package. So, you can safely and easily add StreamSuperLit without thinking about compatibility issues.



## 🛠️ Installing StreamSuperLit

### Install using pip:

1. Clone the repository:
   ```bash
   git clone https://github.com/username/streamsuperlit.git
   cd streamsuperlit
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Install using the GitHub repository:

1. Clone the repository:
   ```bash
   git clone https://github.com/username/streamsuperlit.git
   cd streamsuperlit
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start
In this section, you will quickly learn StreamSuperLit's concepts and how to rewrite your streamlit pages in a modularized reusable way. Let's get started! 😎
### 1. Component
Every widget, visual element (`st.line_plot`, `st.input`, ...), or even an entire page on your project can be though of as a **Component.** In StreamSuperLit, a `Component` is a stateful object whose state is *[magically](#behind-the-scene)* preserved across streamlit reruns. Every `Component` has two important constituents:
- `Controller`: This object controlls the behavior of its associated component. In other words, controller holds any logic related to the behavior of your component.
- `View`: This object defines how the component looks like when it's rendered by streamlit. This object has access to the controller through `self._ctrl` attribute.

You can create a component with the following peice of code:
```python
#  Example Component
from streamsuperlit import Component, View, Controller

class ExampleView(View):
    ...

class ExampleController(Controller):
    ...

# You can alternatively define view and
# controller elsewhere and import them here.
comp_name = 'my_component'
comp_id   = 'a_unique_string_across_the_app'
example_comp = Component(name=comp_name,
                         id=comp_id,
                         view_cls=ExampleView,
                         controller_cls=ExampleController)
```

Notice that for `view_cls` and `controller_cls`, we pass the reference to the <u>*classes*</u>, and not the actual objects. The view and controller objects will be instantiated by the component internally. Also, note that be calling the component object directly (i.e. `__call__`), the component will be rendered. This is the way we ultimately use our components.

⚠️ ***Also, the `id` argument passed to the `Component`'s constructor must be a unique string across all ids in the app.*** ⚠️

### 2. Controller
Controller is an essential part of every StreamSuperLit `Component`. A controller, as its name suggests, controlls the behavior of its component. For example, a controller defines what should happend when a button in the component's view is clicked. The state of the component is also defined in the controller that can be manipulated based on different events. The most important aspect of a controller is the fact that its state is preserved across streamlit reruns.

There are two typical scenarios in which the `View` communicates with the `Controller`:
1. Change in component's state upon an interaction with the view. For example, incrementing a variable once a button is clicked. In such scenarios, you can define a function within your controller and use it in the view like this: `self._ctrl.your_function`.
2. Use the components's state (which is stored as a variable in the controller) to display something in the view. In this case, you access the descired state variable with `self._ctrl.your_state_var`

To create a controller for your component, you need to define a class that inherits the `streamsuperlit.Controller` class. Within this class, you can define your state variables as class attributes inside the `on_init` hook (*<u>not insider the constructor</u>*) and define any method to operate on state variables like this example:

<a id="example-controller"></a>

```python
#  Example Controller
from streamsuperlit import Controller
from streamsuperlit.lifecycle_hook import OnInit

class ExampleController(Controller, OnInit):
    def on_init(self):
        # this line will define a state variable
        # never define your state variables in the constructor
        self.state = 0

    def increment(self):
        # this method is called by the view upon the user
        # clicking on a button
        self.state += 1
```

**You can find full examples [here](#putting-it-together).**

### 3. View
Another essential part of a component is the view object. Using the `View`, you can define how your component looks like. For that, you need to create a class that implements the `_view` method of the abstract class `streamsuperlit.View` like the following example:

<a id="example-view"></a>

```python
#  Example View
from streamsuperlit import View
import streamlit as st

class ExampleView(View):
    def _view(self) -> None:
        col1, col2 = st.columns(2)
        with col1:
            st.text('Hello World!!')
        with col2:
            st.button('click me', on_click=self._ctrl.increment)
            st.text(self._ctrl.state)
```

In the above example, notice a few things:

1. Inside the `_view` method, you can use any Streamlit widget. As mentioned previously, StreamSuperLit is fully compatible with all Streamlit widgets.

2. We updated the state of the component by providing a reference to `self._ctrl.increment` method as the callback function to the button. Now, whenever user clicks on the button, this method in the controller is invoked.
3. Although the app reruns upon each button click, the state of the component is preserved and we accessed it using `self._ctrl.state`. So, the number keeps incrementing instead of being stuck at 0!

### 4. Lifecycle Hooks
When creating a component, it is quite common that you wish to initialize some parameters and define state variables. For that, you can use lifecycle hooks from `streamsuperlit.lifecycle_hook` module. These hooks can be attatched to views and controllers and there are currently two hooks implemented in the package:

- `OnInit.on_init` method: If implemented by the view/controller class, it will be invoked during the component's initialization. This method will be invoked only once and never across reruns. If both the view and the controller of a component implement this method, controller takes precedence over view.
<br>
*<u>This method is generally a good place to initialize your component's state.</u>*

- `AfterInit.after_init` method:  If implemented, it will be invoked after the return of `on_init` on both view and controller. This method will also be invoked only once and never across reruns. If both the view and the controller of a component implement this method, controller takes precedence over view.
### 5. <a id="putting-it-together"></a> Putting It Together
<div style="display:inline; width: fit-content;margin:0;padding:0;"><p style="display: inline">Now, let's put it all together and create a great StreamSuperLit component! </p>💪😎<p style="transform: scale(-1, 1); width: fit-content; display:inline-block;">💪</p></div>

To attach these hooks, the view/controller needs to inherit the hook class and implement the hook method like [this example](#example-controller).

1. Create a directory for your app. I call it `sst_app`. Create the following structure for your project. Of course, this is a recommended structure for large projects (which is inspired by font-end frameworks like [Angular](https://angular.dev)). You can always squeeze everything into just one `app.py`!


```
sst_app/
├── components/                    # This directory holds all components
│   ├── component_one/             # Component directory
│   |   ├── __init__.py            # Component creation is here
│   |   ├── component_one_view.py  # Component's view
│   |   ├── component_one_ctrl.py  # Component's controller
│   ├── component_two/             # You can have multiple components
│   ├── ***
├── pages/                         # Streamlit pages
│   ├── page_one.py                # Here, you can use your components and display them
│   ├── page_two.py                # You can have multiple pages
│   ├── ***
└── app.py                         # The entrypoint to the app

```
2. Let's create one component inside `sst_app/components/component_one/`
    
    - Define the controller like [the above example](#example-controller) in `component_one_ctrl.py`
    - Define the view like [the above example](#example-view) in `component_one_view.py`
    - Define your component like the following snippet in the `__init__.py` of the component directory:

    ```python
    # components/component_one/__init__.py
    from .component_one_view import ComponentOneView
    from .component_one_ctrl import ComponentOneCtrl
    from stremsuperlit import Component

    component_one = Component(name="comp_one",
                              id="unique_id",
                              view_cls=ComponentOneView,
                              controller_cls=ComponentOneCtrl)
    ```
3. Import your component in `pages/page_one.py` and call it like so:

    ```python
    # pages/page_one.py
    from components.component_one import component_one
    from components.component_two import component_two
    import streamlit as st

    st.header('Streamlit widgets and SST components can co-exist in peace!!')
    col1, col2 = st.columns(2)

    with col1:
        component_one()     # Simply call your component and everything will be taken care of!!
    with col2:
        component_two()

    # ... 
    ```

4. Add the following code to the `app.py`, which is just an entrypoint to the app. You can of course use your components here. However in this example, I decided not to.
    ```python
    # app.py
    from streamsuperlit import navigate
    
    if __name__ == "__main__":
        st.set_page_config(layout="wide")
        navigate('main_page')
    ```

5. Run the example application:
   ```bash
   $ python -m streamlit run app.py
   ```

**A fully functioning example can be found [here](example/). But before running the example, you should install the requirements.**

<hr style="margin-top: 50px; opacity:0;"/>

## 🛠️ Behind the Scene
### Project Structure

```
streamsuperlit/
├── dist/                          # Distribution files
├── example/                       # Example application
├── src/streamsuperlit/            # Core library
│   ├── component.py               # Stateful Component implementation
│   ├── controller.py              # Controller logic
│   ├── lifecycle_hook.py          # Lifecycle hook base classes
│   ├── persistent_object.py       # Base class for stateful objects
│   ├── utils.py                   # Helper utilities
│   └── view.py                    # View logic base class
├── LICENSE.txt                    # License information
├── pyproject.toml                 # Project configuration
├── README.md                      # Project documentation
├── requirements.txt               # Dependencies
└── setup.cfg                      # Packaging configuration
```


### Explaining ✨The Magic ✨
The biggest problem with streamlit is that upon user interactions such as button clicks, or using tools like streamlit_autorefresh (for creating live dashboards), the entire application reruns. This causes various issues that make streamlit's caching mechanism (`@st.cache`) rather cumbersome and quirky. By using StreamSuperLit's components, preserving state of objects becomes the default behavior, rather than something you should specify in your code. Now, let's see how it works. Here's an example of vanilla Streamlit page [(you can test it by running the example app)](example/pages/vanilla_streamlit.py):

```python
# app.py
import streamlit as st

# this variable holds the state of the app
a = 0

def increment():
    a += 1

st.button('increment', on_click=increment)
st.text(f'Current value of a: {a}')
```

The expected behavior, from the perspective of a non-streamlit programmer, is that `a` is initialized to 0, and whenever the button is clicked, the number is incremented and the update value would be displayed. However, by running this streamlit page, you'll notice that the displayed values will always remain 0. That's because by clicking the button, the app reruns, so the value of a is again set to 0. This happens with any object you create without using any cache. Here's where *The Magic* comes to the rescue. 

The main idea to create objects whose states are preserved is to somehow save object state in the `streamlit.session_state`. You can think of it as a dictionary of <key: str, value: Object> that is internally preserved by streamlit app across reruns. So now, we know <u>where</u> to store our objects. But how should we store them in such a way that incurs the least amount of boilerplate or burden?

For that, we can use a custom implementaion of `__new__` method for our stateful objects like `Component`. Here's the definition of the `Component` class:

```python
from streamsuperlit.view import View
from streamsuperlit.controller import Controller
from streamsuperlit.lifecycle_hook import OnInit, AfterInit

import streamlit as st

class Component:
    def __new__(cls, name: str, id: str,
                    view_cls: View.__class__,
                    controller_cls: Controller.__class__):
                    if id not in st.session_state:
                        st.session_state[id] = super(Component, cls).__new__(cls)
                    return st.session_state[id]
    def __init__(self, name: str, id: str,
                    view_cls: View.__class__,
                    controller_cls: Controller.__class__) -> None:
        self._name = name
        self._id = id
        
        # ...
```

As you can see here, the trick actually lies within the implementation of `__new__` method. Let's say the app is rerunning and it is executing the following line of code:

```python
# ...
---> component_one = Component(name="comp_one",
                              id="unique_id",
                              view_cls=ComponentOneView,
                              controller_cls=ComponentOneCtrl)
# ...
```
 As with any Python objects, there are two steps involved when instantiating an object:
    1. invoking `__new__`: The actual object creation
    2. invoking `__init__`: Initialization of the object

 By implementing the `__new__` method ourselves, we can take control of how the object is created.
 Therefore, we take advantage of `streamlit.session_state` and upon constructing an object, we first check if its `id` exists 
 in the session state. If so, we do not construct a new object, rather we return the already created instance, hence preserve the 
 state of the object from the last reruns. Otherwise, we do create the object and store it within the session state.

### Utilities
- `get_class`: Dynamically import and resolve a class by its string name.
- `navigate`: Navigate to different Streamlit pages programmatically.

<hr style="margin-top: 50px; opacity: 0"/>


## ⭐ Don't Forget to Star!

If you like this project, please show your support by giving it a **star** on [GitHub](https://github.com/username/streamsuperlit)! 🌟  
Your appreciation keeps me motivated to bring more awesome features to life. 💪  

👉 [Star the project](https://github.com/username/streamsuperlit) and join the journey!


## 🤝 Contribution

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.



## 📫 Contact

For questions, suggestions, or feedback, please open an issue or contact [roohi.abol@gmail.com](mailto:roohi.abol@gmail.com).
## 📝 License

This project is licensed under the [MIT License](LICENSE.txt).

---

