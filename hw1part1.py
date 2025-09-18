import pandas as pd
import numpy as np

# 2% credit
def extract_hour(time):
    """
    Extracts hour information from military time
    
    Args: 
        time (float64): series of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): series of input dimension with hour information.  
          Should only take on integer values in 0-23
    """
    def _hour(x):
        if pd.isna(x):
            return np.nan
        try:
            parts = str(x).split(":")
            if len(parts) != 3:
                return np.nan
            h = int(parts[0]); m = int(parts[1]); s = int(parts[2])
            if 0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59:
                return float(h)
        except Exception:
            pass
        return np.nan
    
    return time.apply(_hour).astype("float64")

# 2% credit
def extract_mins(time):
    """
    Extracts minute information from military time
    
    Args: 
        time (float64): series of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): series of input dimension with minute information.  
          Should only take on integer values in 0-59
    """
    def _mins(x):
        if pd.isna(x):
            return np.nan
        try:
            parts = str(x).split(":")
            if len(parts) != 3:
                return np.nan
            h = int(parts[0]); m = int(parts[1]); s = int(parts[2])
            if 0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59:
                return float(m)
        except Exception:
            pass
        return np.nan
    
    return time.apply(_mins).astype("float64")

# 2% credit
def convert_to_minofday(time):
    """
    Converts HH:MM:SS time to minute of day
    
    Args:
        time: series of time given as strings in HH:MM:SS format.  
          
    
    Returns:
        array (float64): series of input dimension with minute of day
    
    Example: 13:03 is converted to 783.0
    """
    def _conv(s):
        if pd.isna(s):
            return np.nan
        try:
            parts = str(s).split(":")
            if len(parts) != 3:
                return np.nan
            h, m, sec = map(int, parts)
            # Adding this bcoz 24:00:00 is not valid
            if h == 24 and m == 0 and sec == 0:
                return np.nan
            if 0 <= h <= 23 and 0 <= m <= 59 and 0 <= sec <= 59:
                return float(h * 60 + m)
        except Exception:
            return np.nan
        return np.nan
    
    return time_strs.apply(_conv).astype("float64")

# 3%credit
def assigned_scheduled_times(arrival_times, scheduled_times):
    """
    Calculates delay times y - x
    
    Args:
        arrival_times: series of scheduled times 
        scheduled_times: series of actual arrival times
    
    Returns:
        arrival_scheduled_times: pandas dataframe with two columns viz., arrival times and corresponding scheduled time
    """
    
    actual = pd.Series(arrival_times, dtype="float64")
    
    # insert code to find the closest scheduled time for each arrival time in arrival_times
    scheduled = pd.Series(scheduled_times, dtype="float64").dropna().sort_values().to_numpy()
    if scheduled.size == 0:
        return pd.DataFrame({"Arrival Times": actual, "Scheduled Times": np.nan})
    #I'm gonna binary search for nearest schedule time for each arrival
    idx = np.searchsorted(sched, actual.to_numpy())
    left_idx = np.clip(idx - 1, 0, sched.size - 1)
    right_idx = np.clip(idx, 0, sched.size - 1)

    left_vals = sched[left_idx]
    right_vals = sched[right_idx]


    choose_right = (np.abs(right_vals - actual) < np.abs(left_vals - actual))
    assigned = np.where(choose_right, right_vals, left_vals)

    assigned = pd.Series(assigned, index=actual.index)
    assigned[actual.isna()] = np.nan


    return pd.DataFrame({
        "Arrival Times": actual,
        "Scheduled Times": assigned
    })

# 3% credit
def calc_delay(assigned_scheduled_times):
    """
    Calculates delay times y - x
    
    Args:
        assigned_scheduled_times: pandas dataframe with two columns viz., arrival times and corresponding scheduled time
    
    Returns: 
        pandas series of input dimension with delay time
    """
    
    df = assigned_scheduled_times
    print(df)
    

    if 'Arrival Times' in df.columns and 'Scheduled Times' in df.columns:
        scheduled = df['Scheduled Times']
        actual = df['Arrival Times']
    else:
        scheduled = df.iloc[:, 0]
        actual = df.iloc[:, 1]
      
    return (actual.astype('float64') - scheduled.astype('float64')).astype('float64')
