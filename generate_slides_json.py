import os
import json

def generate_slides_json(ppts_folder="assets/img/reports/PPTs", output_folder="assets/img/reports/PPTs"):
    """
    Generates slides.json files in each report's PPT subfolder.

    Args:
        ppts_folder (str): Path to the main PPTs folder.
        output_folder (str): Path where slides.json files will be saved (same as ppts_folder by default).
    """
    for report_folder_name in os.listdir(ppts_folder):
        report_folder_path = os.path.join(ppts_folder, report_folder_name)

        if not os.path.isdir(report_folder_path):
            continue  # Skip if not a directory

        image_files = []
        for filename in os.listdir(report_folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_files.append(filename)

        image_files.sort()  # Ensure slides are in order (alphabetical order of filenames)

        slides_data = []
        for image_file in image_files:
            # Construct image path relative to /assets/img/reports/PPTs/Report X Ppts/
            image_path = f"/FinBlogs/assets/img/reports/PPTs/{report_folder_name}/{image_file}" # Adjust path if needed
            
            # Create object with image property instead of just the path
            slide_object = {"image": image_path}
            slides_data.append(slide_object)

        if slides_data: # Only create json if slides are found
            json_filepath = os.path.join(output_folder, report_folder_name, "slides.json")
            os.makedirs(os.path.dirname(json_filepath), exist_ok=True) # Ensure directory exists
            with open(json_filepath, 'w') as f:
                json.dump(slides_data, f, indent=4)
            print(f"Generated {json_filepath}")
        else:
            print(f"No images found in {report_folder_name}, slides.json not created.")


if __name__ == "__main__":
    # Assuming your image slides will be in FinBlog/PPTs/Report X Ppts/slideX.png
    # and you want to output slides.json in the same folder structure
    generate_slides_json()
    print("JSON files generation completed.")