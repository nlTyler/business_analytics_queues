import math
from idlelib.editor import keynames
from numbers import Number
from wsgiref.util import request_uri
from xml.dom.minidom import NamedNodeMap


def is_valid(lamda, mu, c=1):
    """
        Validates the input parameters.

        Parameters:
        lamda (float or tuple): Arrival rate or rates (tuple for multiple sources).
        mu (float): Service rate.
        c (int, optional): Number of servers. Defaults to 1.

        Returns:
        boolean: True if inputs are valid, False otherwise.
        """
    # validate lambda
    if isinstance(lamda, tuple):
        for i in range(len(lamda)):
            if lamda[i] <= 0:
                return False
    else:
    # ensures lamda is a valid number in a valid format
        if not isinstance(lamda, Number) or (lamda <= 0):
            return False
    # ensures c and mu are in valid formats
    if not isinstance(c, Number) or not isinstance(mu, Number):
        return False
    # checks if c and mu hold valid values
    if (c <= 0 or mu <= 0):
        return False
    return True

# Converts lamda to a tuple if it isn't already and calculates the aggregate arrival rate
def calc_lamda_agg(lamda):
    """
       Converts lambda to a tuple if it isn't already and calculates the aggregate arrival rate.

       Parameters:
       lamda (float or tuple): Arrival rate.

       Returns:
       float: The aggregated arrival rate.
       """
    if isinstance(lamda, tuple):
        w_lamda = lamda
    else:
        w_lamda = (lamda,)
    return sum(w_lamda)

def calc_rho(lamda, mu, c):
    """
        Calculates traffic intensity (rho) and the aggregate arrival rate (r).

        Parameters:
        lamda (float or tuple): Arrival rate or rates.
        mu (float): Service rate.
        c (int): Number of servers.

        Returns:
        tuple: (rho, r) where rho is the traffic intensity and r is the aggregate arrival rate.
        """
    lamda_agg = calc_lamda_agg(lamda)
    r = lamda_agg/mu
    rho = r/c
    return rho, r

def is_feasible(lamda, mu, c=1):
    """
        Checks if the system is feasible (if rho is less than 1).

        Parameters:
        lamda (float, tuple): Arrival rate.
        mu (float): Service rate.
        c (int, optional): Number of servers. Defaults to 1.

        Returns:
        boolean: True if the system is feasible, False otherwise.
        """
    if is_valid(lamda, mu, c):
        rho, r = calc_rho(lamda, mu, c)
        # Ensures rho value is feasible
        if rho >= 1:
            return False
    else:
        return False
    return True

def calc_p0(lamda, mu, c=1):
    """
        Calculate the probability of zero customers in the system (P0).

        Parameters:
        lamda (float, tuple): Arrival rate.
        mu (float): Service rate.
        c (int, optional): Number of servers. Defaults to 1.

        Returns:
        float: Probability P0 if inputs are valid, otherwise returns math.inf or math.nan.
        """

    # Ensures data is valid and feasible before calculations
    if is_valid(lamda, mu, c):
        if is_feasible(lamda, mu, c):
            rho, r = calc_rho(lamda, mu, c)
            # If there is only one server, P0 formula is simplified
            if c >1:
                # Calculates P0
                term1 = sum((r ** i)/math.factorial(i) for i in range(c))
                term2 = (r ** c)/(math.factorial(c)*(1-rho))
                p0 = 1/(term1+term2)
                return p0
            else:
                return 1-rho
        else:
            return math.inf
    else:
        return math.nan

def calc_lq_mmc(lamda, mu, c=1):
    """
        Calculates the average number of customers in the queue for multiple servers.

        Parameters:
        lamda (float, tuple): Arrival rate.
        mu (float): Service rate.
        c (int, optional): Number of servers. Defaults to 1.

        Returns:
        float: Average number of customers in the queue if inputs are valid, otherwise returns math.inf or math.nan.
        """
    # Calculates lq if there is more than one server
    if c != 1:
        # Ensures data is valid and feasible before calculations
        if is_valid(lamda, mu, c):
            if is_feasible(lamda, mu, c):
                # The juicy math happens here to calculate lq
                rho, r = calc_rho(lamda, mu, c)
                p0 = calc_p0(lamda, mu, c)
                num = r ** c * rho
                den = math.factorial(c) * (1-rho) ** 2
                lq = p0*num/den
                return lq
            else:
                return math.inf
        else:
            return math.nan
    else:
        return calc_lq_mm1(lamda, mu, c)

def calc_lq_mm1(lamda, mu, c):
    """
        Calculate the average number of customers in the queue for a single-server system.

        Parameters:
        lamda (float, tuple): Arrival rate or rates.
        mu (float): Service rate.
        c (int): Number of servers (1).

        Returns:
        float: Average number of customers in the queue (lq) if inputs are valid, otherwise returns math.inf or math.nan.
        """
    if is_valid(lamda, mu, c):
        if is_feasible(lamda, mu, c):
            lamda_agg = calc_lamda_agg(lamda)
            lq = lamda_agg**2 / (mu *(mu - lamda_agg))
            return lq
        else:
            return math.inf
    else:
        return math.nan

def calc_bk_mmc(k,lamda, mu, c):
    """
        Calculates the blocking probability in a multi-server queueing model.

        Parameters:
        k (int): The number of servers in the system.
        lamda (float,tuple): The arrival rate to the system.
        mu (float): The service rate.
        c (int): The number of service channels.

        Returns:
        float: The blocking probability (Bk); math.nan if invalid inputs; math.inf if infeasible.
        """
    # Checks if parameters are valid and feasible
    if is_valid(lamda, mu, c):
        if is_feasible(lamda, mu, c):
            # Changes lamda to a tuple if not already
            if not isinstance(lamda, tuple):
                wlamda = (lamda,)
            else:
                wlamda = lamda
            if k != 0:
                if (k <= len(wlamda)) and (k > 0):
                    rhoj = []
                    for l in range(k):
                        rhoj.append(wlamda[l] / (c*mu))
                    # Calculates the blocking probability
                    bk = 1-sum(rhoj)
                    return bk
                else:
                    return math.nan
            else:
                return 1
        else:
            return math.inf
    else:
        return math.nan

def calc_wqk_mmc(k, lamda, mu, c):
    """
        Calculates the expected waiting time in the queue for a specific arrival rate in a multi-server queueing model.

        Parameters:
        k (int): The number of servers in the system.
        lamda (float, tuple): The arrival rate to the system.
        mu (float): The service rate.
        c (int): The number of service channels.

        Returns:
        float: The expected waiting time in the queue (Wqk); math.nan if invalid inputs; math.inf if infeasible.
        """
    # Checks if parameters are valid and feasible
    if is_valid(lamda, mu, c):
        if is_feasible(lamda, mu, c):
            # Changes lamda to a tuple if not already
            if not isinstance(lamda, tuple):
                wlamda = (lamda,)
            else:
                wlamda = lamda
            if k <= len(wlamda):
                # Calculates aggregate arrival rate, rho, average queue length, expected waiting time, and blocking probabilities
                lamda_agg = calc_lamda_agg(lamda)
                rho,r = calc_rho(lamda, mu, c)
                lq = calc_lq_mm1(lamda, mu, c)
                wq = lq/lamda_agg
                bk = calc_bk_mmc(k,lamda, mu, c)
                bk_1 = calc_bk_mmc(k-1, lamda, mu, c)
                # Calculates and returns wqk
                wqk = (1-rho)*wq/(bk*bk_1)
                return wqk
            else:
                return math.nan
        else:
            return math.inf
    else:
        return math.nan


def calc_lqk_mmc(k, lamda, wqk):
    """
        Calculate the expected waiting time in the queue based on k and lamda.

        Parameters:
        k (int): The index of the arrival rate.
        lamda (tuple, list): The arrival rate to the system.
        wqk (float): The waiting time for the specified arrival rate.

        Returns:
        float: The product of the arrival rate at index k-1 and wqk; math.nan if invalid inputs.
        """
    # Ensures lamda is iterable and k is a valid integer
    if not isinstance(lamda, (tuple, list)) or not isinstance(k, int) or not all(isinstance(val, (int, float)) for val in lamda) or (k <= 0) or (k > len(lamda)):
        return math.nan
    # Returns the product of the arrival rate at index k-1 and wqk
    return lamda[k-1] * wqk


def use_littles_law(lamda, mu, c=1, **kwargs):
    """
        Calculates key performance metrics for a queueing system based on Little's Law.

        Parameters:
        lamda (float, tuple): The arrival rate(s) to the system.
        mu (float): The service rate.
        c (int): The number of service channels.
        **kwargs: Additional parameters

        Returns:
        Dictionary: contains lq, l, wq, w, r, rho and also 'wqk' and 'lqk' tuples if queue is a priority queue; math.nan if invalid inputs; math.inf if infeasible.
        """
    # Validate that kwargs only contains valid metric strings
    valid_metrics = ['lq', 'wq', 'w', 'l']
    if not kwargs:
        return None  # Return None if no keyword argument is provided

    # Get the first metric provided in kwargs
    metric = list(kwargs.keys())[0]
    if metric not in valid_metrics:
        raise ValueError(f"Invalid metric '{metric}'. Only 'lq', 'wq', 'w', and 'l' are allowed.")

    # Get the metric value (e.g., 'lq=1.49094')
    kwmetric = kwargs[metric]

    # Check if lamda is a tuple (priority classes) or a single value
    if isinstance(lamda, tuple):
        is_priority = True
        wlamda = sum(lamda)  # Sum of arrival rates for all priority classes

        # Check if any element in lamda is infinite or NaN
        if any(map(math.isinf, lamda)) or any(map(math.isnan, lamda)):
            return float('inf')  # Return inf for infeasible queue
        if any(l < 0 for l in lamda):
            return float('nan')  # Return nan for invalid input
    else:
        is_priority = False
        wlamda = lamda  # Single arrival rate

        # Check if lamda is infinite, NaN, or negative
        if math.isinf(lamda):
            return float('inf')  # Return inf for infeasible queue
        if math.isnan(lamda):
            return float('nan')  # Return nan for invalid input
        if lamda < 0:
            return float('nan')  # Return nan for invalid input

    # Validate mu and c
    if math.isinf(mu) or math.isinf(c):
        return float('inf')  # Return inf for infeasible queue
    if math.isnan(mu) or math.isnan(c):
        return float('nan')  # Return nan for invalid input
    if mu <= 0 or c <= 0:
        return float('nan')  # Return nan for invalid input

    # Avoid division by zero for wlamda
    if wlamda == 0:
        return float('nan')  # Avoid division by zero if wlamda (arrival rate) is zero

    # Create the results dictionary
    littles = {}

    # Calculate the required queue metric
    if metric == 'lq':
        littles['lq'] = kwmetric
    elif metric == 'l':
        littles['lq'] = kwmetric - wlamda / mu
    elif metric == 'wq':
        littles['lq'] = kwmetric * wlamda
    elif metric == 'w':
        littles['lq'] = (kwmetric - 1 / mu) * wlamda
    else:
        return None

    # Use Little's Law to calculate other metrics
    littles['l'] = littles['lq'] + wlamda / mu  # L = Lq + λ/μ
    littles['wq'] = littles['lq'] / wlamda  # Wq = Lq / λ
    littles['w'] = littles['wq'] + 1 / mu  # W = Wq + 1/μ
    littles['r'] = wlamda / mu  # Utilization (ρ = λ / μ)

    # Calculate utilization for multiple servers
    littles['ro'] = littles['r'] / c  # ro is the utilization per server

    # Handle priority classes if applicable
    if is_priority:
        wqk = []
        lqk = []
        for i in range(len(lamda)):
            k = i + 1  # Assuming k is the class index (starting from 1)
            wq = calc_wqk_mmc(k, lamda[i], mu, c)  # Changed order to (k, lamda, mu, c)
            # Append valid calculated values
            if not math.isnan(wq):
                wqk.append(wq)
                lqk.append(wq * lamda[i])
            else:
                wqk.append(float('nan'))
                lqk.append(float('nan'))

        # Always include 'wqk' and 'lqk' in the result, but ensure valid values
        littles['wqk'] = tuple(wqk)
        littles['lqk'] = tuple(lqk)

    # Check if we are expecting a single real number like inf or nan
    if math.isinf(kwmetric) or math.isnan(kwmetric):
        return kwmetric

    # Return the results dictionary for valid cases
    return littles

