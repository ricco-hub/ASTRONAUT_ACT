from pathlib import Path
from astropy.io import fits

MODULE_DIR = Path(__file__).resolve().parent
FILE_PATH = MODULE_DIR / "asteroid_list.txt"


def ast_names() -> None:
    """
    Print available asteroid names in the API
    """

    # Create a set to store unique parts of the strings
    unique_parts = set()

    with open(FILE_PATH, "r") as file:
        for line in file:
            # Strip any leading/trailing whitespace (including newlines)
            cleaned_line = line.strip()

            underscore_index = cleaned_line.find("_")

            # Extract the part of the string before the first underscore
            if underscore_index != -1:
                part = cleaned_line[:underscore_index]
                unique_parts.add(part)

    sorted_unique_parts = sorted(unique_parts)

    for part in sorted_unique_parts:
        print(part)


def find_ast(ast: str) -> None:
    """
    Input: asteroid name
    Output: print current asteroids in API
    """

    with open(FILE_PATH, "r") as file:
        for line in file:
            if ast in line:
                print(line, end="")
            else:
                continue


def find_arr(arr: str) -> None:
    """
    Input: ACT array: pa4, pa5, pa6
    Output: print current asteroids in API corresponding to arr
    """

    with open(FILE_PATH, "r") as file:
        for line in file:
            if arr in line:
                print(line, end="")
            else:
                continue


def find_freq(freq: str) -> None:
    """
    Input: frequency (GHz): 090, 150, 220
    Output: print current asteroids in API corresponding to freq
    """

    with open(FILE_PATH, "r") as file:
        for line in file:
            if freq in line:
                print(line, end="")
            else:
                continue


def inv_var(data: list[float], variances: list[float]) -> tuple[float, float]:
    """
    Inputs: data, list of data 
            variances, list of variances associated with data
    Outputs: inverse variance weighted average and inverse variance
    """

    ave = 0
    var = 0
    for i in range(len(data)):
        ave += data[i]/variances[i]
        var += 1/variances[i]
    return ave/var, 1/var


def get_ast_weighted_flux(ast: str, array: str, freq: str) -> tuple[float, float]:
    """
    Inputs: ast, name of asteroid
            array, ACT array: pa4, pa5, pa6
            freq, frequency (GHz): 090, 150, 220
    Outputs: weight_flux, inverse variance weighted flux
             weight_var, inverse variance
    """

    name = f'{ast}_lc_{array}_{freq}'

    s3_path = 's3://cornell-acteroids/' + name + '.fits'
    with fits.open(s3_path, fsspec_kwargs={"anon": True}) as hdul:  
        data = hdul[1].data
    # get data from each column
    flux = data['Flux']
    error = data['FluxUncertainty']
    weight = data['Weight']
    weight_flux, weight_var = inv_var(flux*weight, (error*weight)**2) # Inverse variance weighted ACT flux scaled to 1au/1au/alpha0

    return weight_flux, weight_var