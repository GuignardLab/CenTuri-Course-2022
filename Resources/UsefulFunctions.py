import matplotlib.pyplot as plt
import numpy as np

def da_alone(a, dt, k):
    """
    Computes the change of concentration given an initial concentration `a`,
    a time increment `dt` and a constant `k`. Note that there is no `i` in
    the equation since it is supposed to be `a` alone.
    
    Args:
        a (float): The initial concentration value
        dt (float): the time increment
        k (float): the constant k

    Returns:
        (float): the change of concentration
    """
    return dt * (a - a**3 + k)

def da(a, i, dt, k):
    """
    Computes the change of concentration given an initial concentration `a`,
    a time increment `dt` and a constant `k`.

    Args:
        a (float): the initial concentration value
                   of the activator
        i (float): the initial concentration value
                   of the inhibitor
        dt (float): the time increment
        k (float): the constant k

    Returns:
        (float): the change of concentration
    """
    return dt * (a - a**3 - i + k)

def di(i, a, dt, tau):
    """
    Computes the change of concentration given an initial concentration `i`,
    a time increment `dt` and a constant `k`.

    Args:
        a (float): the initial concentration value
                   of the activator
        i (float): the initial concentration value
                   of the inhibitor
        dt (float): the time increment
        tau (float): the constant tau

    Returns:
        (float): the change of concentration
    """
    return dt/tau * (a - i)

def plot_concentration_1cell(c1, c2=None, return_plot=False, save_path=None):
    """
    Plots the concentration evolution given a list of concentrations

    Args:
        c1 (list of floats): a list containing concentrations
        c2 (Optional, list of floats): a list containing concentrations
    """
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(c1, label='First concentration')
    if c2 is not None:
        ax.plot(c2, label='Second concentration')
        ax.legend()
    ax.set_xlabel('Time-point')
    ax.set_ylabel('Concentration')
    fig.tight_layout()
    if save_path is not None:
        save_path = save_path.with_suffix('.png')
        plt.savefig(save_path)
        plt.close(fig)
    if return_plot:
        return fig, ax

def plot_concentration_1D(c1, c2=None, return_plot=False,
                          save_path=None, step=100):
    """
    Plots the concentration evolution given 1 or 2 array(s) of cells
    and concentrations. When two array are combined, the firs concentration
    is in the green and the second in the red. Both values are mixed.

    Args:
        c1 ndarray (n, m): array of concentration of n cells
                           over m time-points
        c2 ndarray (n, m): array of concentration of n cells
                           over m time-points
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    if c2 is None:
        im = ax.imshow(c1[:, ::step], interpolation='nearest')
        cbar = plt.colorbar(im)
        cbar.set_label('Concentration')
    else:
        max_ = np.max([c1, c2])
        min_ = np.min([c1, c2])
        rgb = np.array([c1, c2, np.zeros_like(c1)]).transpose(1, 2, 0)
        rgb = (rgb-min_)/(max_-min_)
        im = ax.imshow(rgb[:,::step,:], interpolation='nearest')
    ax.set_xlabel('Time-point')
    ax.set_ylabel('Cell #')
    ax.set_xticks(np.linspace(0, c1.shape[1]//step, 6).astype(int)[:-1])
    ax.set_xticklabels([f'{v*step:.0f}' for v in ax.get_xticks()])
    fig.tight_layout()
    if save_path is not None:
        save_path = save_path.with_suffix('.png')
        plt.savefig(save_path)
        plt.close(fig)
    if return_plot:
        return fig, ax

def __compute_AI(a, i, dt, k, tau, n):
    A, I = [a], [i]
    for t in range(n-1):
        new_A = A[-1] + da(A[-1], I[-1], dt, k)
        new_I = I[-1] + di(I[-1], A[-1], dt, tau)
        I.append(new_I)
        A.append(new_A)
    return A, I

def retrieve_compute_AI():
    """
    Returns the function compute_AI
    """
    return __compute_AI

def __get_random_table(n, m, seed=0):
    np.random.seed(seed)
    return np.random.rand(n, m)

def get_random_table(n, m, seed=0):
    """
    Return a array of size n by m filled with
    random values between 0 and 1. The random
    values will always be the same thanks to the
    seed. The seed can be changed

    Args:
        n (int): first dimension of the array
        m (int): second dimension of the array
        seed (int): Determine the seed for the
                    random draw. Default 0.
                    If None, it will be different
                    each time it is ran.

    Returns:
        ndarray (n, m)
    """
    # Nope, you will not see the code in here!
    # I mean, if you really want to you can,
    # but that's cheating ...
    return __get_random_table(n, m, seed=seed)

def __question_4(*, A, I, dt, k, tau, n):
    if not isinstance(A, list):
        A = [A]
    if not isinstance(I, list):
        I = [I]
    for t in range(n):
        new_A = A[-1] + da(A[-1], I[-1], dt, k)
        new_I = I[-1] + di(I[-1], A[-1], dt, tau)
        I.append(new_I)
        A.append(new_A)
    return A, I

def __question_13(*, A, I, dt, k, tau, n):
    A = np.copy(A)
    I = np.copy(I)
    for cell_num, (a, i) in enumerate(zip(A[:, 0], I[:, 0])):
        A_cell, I_cell = __compute_AI(a, i, dt, k, tau, n)
        A[cell_num, :] = A_cell
        I[cell_num, :] = I_cell
    return A, I

results_dict = {
    4: __question_4,
    13: __question_13
}

params_dict = {
    4: """
    For this function, the following calling
    is expected (changing val as needed):
    answer_results(4, A=[<val>], I=[<val>],
                   dt=<val>, k=<val>, tau=<val>)
    """,
    13: """
    For this function, the following calling
    is expected (changing val as needed):
    answer_results(13, A=A, I=I,
                   dt=<val>, k=<val>, tau=<val>)
    With A and I you tables with the first value
    initialized.
    """
}

def answer_results(q, **kwargs):
    """
    Returns the expected out for the question `q`

    Args:
        q (int): the number of the question
        kwargs: the potential args of question q

    Returns:
        ??? It depends on which question was asked
    """
    if q in results_dict:
        try:
            out = results_dict[q](**kwargs)
        except Exception as e:
            print(e)
            print(params_dict.get(q, 'Unfortunately, no more help is there :/'))
            out = None
    else:
        print(f'Question {q} were not found')
        out = None
    return out