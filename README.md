# Air-stripping-column
### Programing method:
- The program design stages were accomplished using Python programming. The design is flexible and can accommodate new compounds and packing materials, utilizing three JSON files: "Pack" to select the desired packing material, "ppow" containing required properties for water and temperature based on the selected temperature, and "value" containing different types of contaminants and their corresponding properties such as molecular weight, atomic volume, and diffusion volume.
- Manual entry is required for the contaminant name, temperature, discharge Q (m^3/day), a first assumption of stripping factor, and effluent and influent concentration. The other data is either automatically computed or picked from the Jason files.
- To obtain accurate outputs, the program was coded in the function way , bringing together data to make it easier to understand how the program works. The Python script includes various libraries, such as "JSON" for loading and parsing JSON files, "math" for mathematical operations, "tkinter" for creating a graphical user interface (GUI), "Numpy" for numerical computing and creating arrays, and "matplotlib" for creating plots and graphs.