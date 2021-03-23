from pidcontroller import Variable, PIDController
import time
if __name__ == "__main__":
    V_input = Variable(name="input")
    V_output = Variable(name="output")
    V_observable = Variable(name="observable")
    controller = PIDController(1e-1, 1e-1, 1e-1, V_input, V_output, V_observable)

    @controller.observable_observe
    def sysEstim(x):
        return x

    @controller.input_observe
    def makeInput(x):
        return x
    makeInput(10)
    for i in range(100):
        time.sleep(0.01)
        sysEstim(V_output.value)
    controller.visualize()