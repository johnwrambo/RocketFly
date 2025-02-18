import matplotlib
matplotlib.use("TkAgg")  # Or try "Agg", "Qt5Agg", or "MacOSX" depending on your OS
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

def plot_fun(x,y,label_text: str = None):

    plt.plot(x, y,label= label_text)
    plt.xlabel('x')
    plt.ylabel(label_text)
    plt.title(f'Plot {label_text}')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_animation(x,y,t_span,INITIAL_VELOCITY,LAUNCH_ANGLE):

    fig, ax = plt.subplots()
    ax.set_xlim(0, max(x) + 10)  # Set x limits
    ax.set_ylim(0, max(y) + 10)  # Set y limits
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title(f"Launch {INITIAL_VELOCITY} m/s at {np.degrees(LAUNCH_ANGLE)}°")
    ax.grid(True)

    # Create an empty line object
    line, = ax.plot([], [], 'bo-', lw=2)  # 'bo-' = blue dots connected with a line

    # **Update function for animation**
    ground_index = np.argmax(y < 0) if np.any(y < 0) else len(y) - 1  # Stop at last frame if y never < 0

    global start_time
    start_time = None  # Will be set in the first frame

    def update(frame):
        global start_time
        if start_time is None:
            start_time = time.time()  # Start timer on first frame

        if frame >= ground_index:  # Stop when y reaches ground (y < 0)
            ani.event_source.stop()  # Stop animation
        """Updates the plot frame by frame"""
        line.set_data(x[:frame], y[:frame])  # Update x, y values incrementally
        print(y[frame])
        end_time = time.time()  # Stop timer on last frame
        elapsed_time = end_time - start_time
        print(f"Animation runtime: {elapsed_time:.4f} seconds")
        return line,

    # **Create real-time animation**
    start_time = time.time()
    ani = animation.FuncAnimation(fig, update, frames=len(t_span), interval=30, blit=True)
    end_time = time.time()
    plt.show()  # Display the animated plot
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")
