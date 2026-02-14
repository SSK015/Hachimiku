"""
Label generation utilities for creating common label sequences.
"""

class LabelGenerator:
    """Helper class for generating chart labels with various patterns"""
    
    @staticmethod
    def linear(start: float, count: int, step: float = 1, prefix: str = "", suffix: str = "") -> list:
        """
        Generate linear sequence labels (e.g., 1, 2, 3, 4)
        
        Args:
            start: Start value
            count: Number of labels
            step: Increment step
            prefix: Prefix for each label
            suffix: Suffix for each label
        
        Returns:
            list: List of label strings
        """
        # Determine if we should treat as integer or float
        is_int = isinstance(start, int) and isinstance(step, int)
        
        labels = []
        for i in range(count):
            val = start + i * step
            if is_int:
                val_str = str(int(val))
            else:
                val_str = f"{val:.2f}".rstrip('0').rstrip('.')
            labels.append(f"{prefix}{val_str}{suffix}")
            
        return labels

    @staticmethod
    def exponential(base: float, start_exp: float, count: int, format_str: str = "{:.0g}") -> list:
        """
        Generate exponential sequence values (e.g., 1, 10, 100)
        
        Args:
            base: Base number
            start_exp: Starting exponent
            count: Number of labels
            format_str: Format string for values
            
        Returns:
            list: List of label strings
        """
        return [format_str.format(base**(start_exp + i)) for i in range(count)]

    @staticmethod
    def power_notation(base: int, start_exp: int, count: int, math_mode: bool = True) -> list:
        """
        Generate power notation labels (e.g., 2^0, 2^1, 2^2)
        
        Args:
            base: Base number
            start_exp: Starting exponent
            count: Number of labels
            math_mode: Whether to wrap in LaTeX math delimiters ($...$)
            
        Returns:
            list: List of label strings
        """
        labels = []
        for i in range(count):
            exp = start_exp + i
            if math_mode:
                labels.append(f"${base}^{{{exp}}}$")
            else:
                labels.append(f"{base}^{exp}")
        return labels
        
    @staticmethod
    def custom(func, count: int, start_index: int = 0) -> list:
        """
        Generate custom labels using a function
        
        Args:
            func: Function that takes an index and returns a label string
            count: Number of labels
            start_index: Starting index passed to func
            
        Returns:
            list: List of label strings
        """
        return [str(func(start_index + i)) for i in range(count)]

    @staticmethod
    def memory_size(values_in_bytes: list, binary: bool = True) -> list:
        """
        Format a list of byte values into human-readable memory sizes (K, M, G, etc.)
        
        Args:
            values_in_bytes: List of numbers representing sizes in bytes
            binary: Whether to use binary prefixes (1024) or decimal (1000)
            
        Returns:
            list: Formatted strings
        """
        unit = 1024 if binary else 1000
        suffixes = ['', 'K', 'M', 'G', 'T', 'P']
        
        labels = []
        for val in values_in_bytes:
            if val is None or val == "":
                labels.append("")
                continue
            if val == 0:
                labels.append('0')
                continue
            
            # Find the appropriate suffix
            i = 0
            temp_val = float(val)
            while temp_val >= unit and i < len(suffixes) - 1:
                temp_val /= unit
                i += 1
            
            # Format value: remove .0 if it's an integer
            val_str = f"{temp_val:.1f}".rstrip('0').rstrip('.')
            labels.append(f"{val_str}{suffixes[i]}")
            
        return labels

    # Preset label lists
    PRESETS = {
        'paper_memory': ['1024', '', '1M', '', '32M', '', '64M', '', '256M', '', '1G']
    }


