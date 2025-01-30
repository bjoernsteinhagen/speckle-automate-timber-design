> ⚠️ This automation is provided as-is and should be thoroughly tested before implementation in production environments. While the code performs timber column design checks according to Eurocode 5, it is the engineer's responsibility to verify all results and ensure compliance with local regulations and standards.

# 🤖 Timber Design
## 📋 Overview
Automated design validation for timber columns in ETABS models, triggered on every model change to ensure continuous compliance checks.

## 🎯 Purpose & Benefits

### For Structural Engineers Who...
* Spend hours **manually transferring** analysis results from ETABS to standalone design software (mb, FRILLO, Excel etc.)
* Need to keep elemental designs in **sync** with their global model
* Want to **eliminate errors** from manual calculations and data entry

### Before Automate
* **Disconnected workflows** between global analysis and element design
* **Time lost** to manual data transfer
* Risk of errors when analysis results change but **element designs aren't updated**
* Difficulty tracking design iterations and changes

### After Automate
* Real-time timber column design checks using your ETABS model data
* Integration of Eurocode 5 requirements
* Immediate feedback when model changes affect column design compliance
* Automatic processing of:
  * Object types (filters columns with timber material designation)
  * Analysis results
  * Geometric properties
  * Material definitions

## ⚙️ Setup
|   |   |
|---|---|
|__Source Application__| ETABS |
|__Connector Version__| v2.x |
|__Send Configuration__| Everything (with analysis results) |

### Function Inputs
<img src="https://github.com/user-attachments/assets/915e750f-89a5-4b71-a916-4a7fd5c6f2ea" width="50%" />

### Send
* Ensure that the `Selection` is set to `everything` and that analysis results are also sent.
<img src="https://github.com/user-attachments/assets/1058f972-0484-44ed-b03c-31be5ada7abd" width="50%" />

### Caveats
* Materials are parsed according to their `Material Name` in ETABS. Columns are identified as timber if their assigned `material` matches the available timber grades for the selected region. For `Britain`, the available grades are: `C16`, `C24`, `C27`, `GL24c`, `GL28c`, `GL32c`, `GL24h`, `GL28h`, `GL32h`.
* Available regions and associated grades can be extended by editing `materials.py` in the repository.
<img width="386" alt="image" src="https://github.com/user-attachments/assets/54000fad-ef00-46d4-b954-f5a3a04d2631" />

* Available design codes can be extended by adding a new class to `src/design`. Follow the pattern of `eurocode.py` (the implementation must inherit from the base class `DesignCode`.
* The `sourceApplication` can be extended beyond ETABS. For this, add a new class to `src/model`. Follow the pattern of `etabs.py` (the implementation must inherit from the base class `StructuralModel`.

## 📈 Results & Validation
The model which triggers the automation has summary automation results which can be interrogated. In the below screenshot, we can for example filter the checked timber columns by those with a utilization between 0.75 and 1.0:

<img width="1280" alt="image" src="https://github.com/user-attachments/assets/687ffa6d-5e11-45b2-8f26-c73ba53a019a" />

For more granular calculation steps, we can open the provided "Model for writing results". Here 3D utilization plots can be federated with the triggering model for greater context. Furtherore, the objects have the metadata from each calculation step attached. These can be seen by the selection information on the right of the viewer:

![image](https://github.com/user-attachments/assets/ee71328d-a6af-4202-b918-a52687eb62f0)



### 🟢 SUCCEEDED
What constitutes a successful run:
* The `sourceApplication` is identified as ETABS
* The Speckle model has was sent using "Everything". This means that `specs` and `elements` attributes exist
* If at least one column could be processed. This entails:
  * Object having a valid `length` attribute
  * Object `cross_section` being rectangular
  * Object `material` being parsed as timber
  * Object containing `forces` from the analysis results
* A timber column failing the design check (utilization > 1.0) will still be deemed as successful automation run

### 🔴 FAILED
What constitutes a failed run:
* The inverse of criteria for a successful run:
  * `sourceApplication` not ETABS
  * Not a single designable timber column found

## 📚 Additional Information
### Version History
| Version | Date | Changes |
|---------|------|---------|
| v0.1.0-alpha | 2025-12-05 | For testing. |
