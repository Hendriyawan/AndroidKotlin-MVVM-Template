# ANDROID CLEAN MVVM TEMPLATE

This repository provides an automation tool to generate boilerplate for an **Android Clean Architecture + MVVM** project using [Mason CLI](https://github.com/felangel/mason). 

## 📺 Demos

### 1. Generate Mason Bricks
![Generate Mason Bricks](run_script_generate_template.mov)

### 2. Execute Templates in Project
![Execute Templates](run_make_to_project.mov)

With this tool, you no longer need to waste time manually creating repetitive setups or writing the Clean Architecture folder structure in your Android Kotlin project.

## 🚀 Features

There is a Python script (`create_android_mvvm_template.py`) that, when executed, generates two **Mason Bricks**:
1. **`android_core_setup`**: Generates the boilerplate for the Core layer (DI, Network, Base Classes, Resources, Application class, etc.) and the basic App structure (Gradle scripts). You only need to run this **once** when initializing a project.
2. **`android_feature`**: Generates the file structure for a new feature (Domain Repository Interface, Data Repository Impl, ViewModel, and Fragment) following Clean Architecture principles. You can run this **multiple times** whenever you create a new feature.

---

## 🛠️ Requirements

Make sure you have [Mason CLI](https://docs.brickhub.dev/) installed on your machine. If not, install it using Dart:
```bash
dart pub global activate mason_cli
```

---

## 📖 How to Use

### 1. Generate Mason Bricks
First, you need to run the Python script to build the brick templates:
```bash
python create_android_mvvm_template.py
```
> **Note:** Once the script finishes, the two folders (`android_core_setup` and `android_feature`) will be automatically created directly inside your `$HOME/.bricks` directory.

### 2. Initialize Mason (If Not Yet Initialized)
Open your terminal and navigate to the root directory of your target Android project. If your project doesn't use Mason yet, run:
```bash
mason init
```

### 3. Add Bricks to Your Project
Register the two newly generated bricks into your project:
```bash
mason add android_core_setup --path ~/.bricks/android_core_setup
mason add android_feature --path ~/.bricks/android_feature
```

### 4. Execute the Templates

#### A. Setup Core Project (Run Once)
To initialize the Android project with base structure and core classes, run:
```bash
mason make android_core_setup
```
Mason will prompt you for:
- `package_name` (e.g., `com.example.myapp`)
- `app_name` (e.g., `App` or `MyApp`)

Or you can bypass the prompt with arguments:
```bash
mason make android_core_setup -c package_name=com.example.myapp -c app_name=MyApp
```

#### B. Generate a New Feature
When you want to create a new feature module (e.g., "Article" feature), run:
```bash
mason make android_feature
```
Mason will prompt you for:
- `package_name` (e.g., `com.example.myapp`)
- `feature_name` (e.g., `Article`)

Or run it directly with arguments:
```bash
mason make android_feature --package_name=com.example.myapp --feature_name=Article
```

This will automatically create the following folder hierarchy and files:
- `domain/repository/ArticleRepository.kt`
- `data/repository/ArticleRepositoryImpl.kt`
- `presenter/article/ArticleViewModel.kt`
- `presenter/article/ArticleFragment.kt`

---

## 📂 Generated Directory Structure

**Core Setup (`android_core_setup`)** generates:
- `app/src/main/java/com/.../core/`
- `app/src/main/java/com/.../data/source/`
- `app/src/main/java/com/.../domain/model/Resource.kt`
- `app/src/main/java/com/.../<AppName>.kt` (Application Class)
- Various related gradle files (e.g., `gradle/libs.versions.toml`)

**Feature Setup (`android_feature`)** generates (inside your package):
- `domain/repository/<FeatureName>Repository.kt`
- `data/repository/<FeatureName>RepositoryImpl.kt`
- `presenter/<feature_name>/<FeatureName>ViewModel.kt`
- `presenter/<feature_name>/<FeatureName>Fragment.kt`
