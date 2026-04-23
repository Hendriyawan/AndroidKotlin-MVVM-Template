import os
import shutil

home_dir = os.path.expanduser("~")
base_templates_dir = f"{home_dir}/.bricks"

#configure default values from local.properties
DEFAULT_BASE_URL = "https://newsapi.org/"
DEFAULT_API_KEY = ""

if os.path.exists("local.properties"):
    with open("local.properties", "r") as f:
        for line in f:
            if line.startswith("API_KEY="):
                val = line.split("=")[1].strip()
                if val: DEFAULT_API_KEY = val
            if line.startswith("BASE_URL="):
                val = line.split("=")[1].strip()
                if val: DEFAULT_BASE_URL = val

#clean old bricks if exists
if os.path.exists(f"{base_templates_dir}/android_core_setup"):
    shutil.rmtree(f"{base_templates_dir}/android_core_setup")
if os.path.exists(f"{base_templates_dir}/android_feature"):
    shutil.rmtree(f"{base_templates_dir}/android_feature")

os.makedirs(base_templates_dir, exist_ok=True)

def create_dir(path):
    os.makedirs(path, exist_ok=True)

# ---------------------------------------------------------
# BRICK 1: android_core_setup
# ---------------------------------------------------------
core_brick = "android_core_setup"
core_dir = f"{base_templates_dir}/{core_brick}/__brick__"
core_src_dir = f"{core_dir}/app/src/main/java/{{{{package_name.pathCase()}}}}"

create_dir(core_src_dir)
create_dir(f"{core_dir}/app")
create_dir(f"{core_dir}/gradle")

with open(f"{base_templates_dir}/{core_brick}/brick.yaml", "w") as f:
    f.write(f"""name: android_core_setup
description: Advanced Clean Architecture Core Setup (DI, Room, Retrofit, Full Gradle Configuration)
version: 1.0.0
vars:
  package_name:
    type: string
    default: "com.example.app"
  app_name:
    type: string
    default: "MyAwesomeApp"
  base_url:
    type: string
    default: "{DEFAULT_BASE_URL}"
  api_key:
    type: string
    default: "{DEFAULT_API_KEY}"
""")

# --- ROOT GRADLE FILES ---

with open(f"{core_dir}/build.gradle.kts", "w") as f:
    f.write("""
// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.hilt.android) apply false
    alias(libs.plugins.ksp) apply false
    alias(libs.plugins.kotlin.parcelize) apply false
}
""")

with open(f"{core_dir}/settings.gradle.kts", "w") as f:
    f.write("""pluginManagement {
    repositories {
        google {
            content {
                includeGroupByRegex("com\\\\.android.*")
                includeGroupByRegex("com\\\\.google.*")
                includeGroupByRegex("androidx.*")
            }
        }
        mavenCentral()
        gradlePluginPortal()
    }
}
plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "{{app_name}}"
include(":app")
""")

with open(f"{core_dir}/gradle/libs.versions.toml", "w") as f:
    f.write("""
[versions]
# Core & Build
agp = "9.1.0"
kotlin = "2.3.20"
ksp = "2.3.6"
coreKtx = "1.18.0"

# UI components
appcompat = "1.7.1"
material = "1.13.0"
activity = "1.13.0"
constraintlayout = "2.2.1"
fragment = "1.8.9"
annotation = "1.9.1"
splashscreen = "1.2.0"
glide = "5.0.5"
swiperefreshlayout = "1.1.0"

# Architecture Components
lifecycle = "2.10.0"

# Dependency Injection
hilt = "2.59.2"

# Networking
retrofit = "3.0.0"
convertGson = "3.0.0"
loggingInterceptor = "5.3.2"
gson = "2.13.2"

# Local Database
room = "2.8.4"

# Testing
junit = "4.13.2"
junitVersion = "1.3.0"
espressoCore = "3.7.0"
coroutinesTest = "1.10.2"
mockito = "5.23.0"
mockitoKotlin = "6.3.0"
archCoreTest = "2.2.0"

# Browser
browser = "1.10.0"


[libraries]
# AndroidX
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
androidx-appcompat = { group = "androidx.appcompat", name = "appcompat", version.ref = "appcompat" }
androidx-activity = { group = "androidx.activity", name = "activity", version.ref = "activity" }
androidx-constraintlayout = { group = "androidx.constraintlayout", name = "constraintlayout", version.ref = "constraintlayout" }
androidx-annotation = { group = "androidx.annotation", name = "annotation", version.ref = "annotation" }
splashscreen = { group = "androidx.core", name = "core-splashscreen", version.ref = "splashscreen" }
androidx-fragment-ktx = { group = "androidx.fragment", name = "fragment-ktx", version = "fragment" }
androidx-browser = { group = "androidx.browser", name="browser", version.ref = "browser"}
androidx-swiperefreshlayout = { group = "androidx.swiperefreshlayout", name = "swiperefreshlayout", version.ref = "swiperefreshlayout" }

# Material
material = { group = "com.google.android.material", name = "material", version.ref = "material" }

# Lifecycle
androidx-lifecycle-livedata-ktx = { group = "androidx.lifecycle", name = "lifecycle-livedata-ktx", version.ref = "lifecycle" }
androidx-lifecycle-viewmodel-ktx = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-ktx", version.ref = "lifecycle" }

# Dependency Injection
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }

# Networking & Serialization
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
converter-gson = { group = "com.squareup.retrofit2", name = "converter-gson", version.ref = "convertGson" }
logging-interceptor = { module = "com.squareup.okhttp3:logging-interceptor", version.ref = "loggingInterceptor" }
gson = { group = "com.google.code.gson", name = "gson", version.ref = "gson" }

# Room
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }

# Glide
glide = { group = "com.github.bumptech.glide", name = "glide", version.ref = "glide" }
glide-compiler = { group = "com.github.bumptech.glide", name = "compiler", version.ref = "glide" }

# Testing
junit = { group = "junit", name = "junit", version.ref = "junit" }
androidx-junit = { group = "androidx.test.ext", name = "junit", version.ref = "junitVersion" }
androidx-espresso-core = { group = "androidx.test.espresso", name = "espresso-core", version.ref = "espressoCore" }
kotlinx-coroutines-test = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-test", version.ref = "coroutinesTest" }
mockito-core = { group = "org.mockito", name = "mockito-core", version.ref = "mockito" }
mockito-kotlin = { group = "org.mockito.kotlin", name = "mockito-kotlin", version.ref = "mockitoKotlin" }
androidx-arch-core-testing = { group = "androidx.arch.core", name = "core-testing", version.ref = "archCoreTest" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
hilt-android = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
kotlin-parcelize = { id = "org.jetbrains.kotlin.plugin.parcelize", version.ref = "kotlin"}
""")

# --- APP GRADLE FILE ---

with open(f"{core_dir}/app/build.gradle.kts", "w") as f:
    f.write("""
import java.util.Properties
import java.io.FileInputStream

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.hilt.android)
    alias(libs.plugins.ksp)
    alias(libs.plugins.kotlin.parcelize)
    id("kotlin-parcelize")
}

android {
    namespace = "{{package_name}}"
    compileSdk = 35

    defaultConfig {
        applicationId = "{{package_name}}"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        val properties = Properties()
        val localPropertiesFile = rootProject.file("local.properties")
        if (localPropertiesFile.exists()) {
            properties.load(FileInputStream(localPropertiesFile))
        }

        val apiKey = properties.getProperty("API_KEY") ?: "{{api_key}}"
        val baseUrl = properties.getProperty("BASE_URL") ?: "{{base_url}}"

        buildConfigField("String", "API_KEY", "\\"$apiKey\\"")
        buildConfigField("String", "BASE_URL", "\\"$baseUrl\\"")
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlin {
        jvmToolchain(17)
    }
    buildFeatures {
        buildConfig = true
        viewBinding = true
    }
    packaging {
        resources {
            excludes += "META-INF/{AL2.0, LGPL2.1}"
        }
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
    implementation(libs.androidx.activity)
    implementation(libs.androidx.constraintlayout)
    implementation(libs.androidx.annotation)
    implementation(libs.androidx.lifecycle.livedata.ktx)
    implementation(libs.androidx.lifecycle.viewmodel.ktx)
    implementation(libs.androidx.fragment.ktx)
    implementation(libs.androidx.swiperefreshlayout)
    implementation(libs.splashscreen)
    implementation(libs.androidx.browser)

    // DI
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)

    // Network
    implementation(libs.retrofit)
    implementation(libs.converter.gson)
    implementation(libs.logging.interceptor)
    implementation(libs.gson)

    // Local
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)

    // Image
    implementation(libs.glide)
    ksp(libs.glide.compiler)

    // Testing
    testImplementation(libs.junit)
    testImplementation(libs.kotlinx.coroutines.test)
    testImplementation(libs.mockito.core)
    testImplementation(libs.mockito.kotlin)
    testImplementation(libs.androidx.arch.core.testing)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
}
""")

# --- CORE SOURCE CODE ---

create_dir(f"{core_src_dir}/core/utils")
create_dir(f"{core_src_dir}/core/di")
create_dir(f"{core_src_dir}/domain/model")
create_dir(f"{core_src_dir}/data/repository")
create_dir(f"{core_src_dir}/data/source/remote")
create_dir(f"{core_src_dir}/data/source/local/room/database")
create_dir(f"{core_src_dir}/data/source/local/room/dao")

with open(f"{core_src_dir}/core/Constants.kt", "w") as f:
    f.write("""
package {{package_name}}.core
object Constants { const val DATABASE_NAME = "app_database.db" }
""")

with open(f"{core_src_dir}/core/Extensions.kt", "w") as f:
    f.write("""
package {{package_name}}.core
import android.content.Context
import android.content.Intent
import android.os.Parcelable
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit

inline fun <reified T : Any> Context.startActivity(vararg params: Pair<String, Any?>) {
    val intent = Intent(this, T::class.java)
    params.forEach { (key, value) ->
        when (value) {
            is Int -> intent.putExtra(key, value)
            is String -> intent.putExtra(key, value)
            is Double -> intent.putExtra(key, value)
            is Boolean -> intent.putExtra(key, value)
            is Parcelable -> intent.putExtra(key, value)
        }
    }
    startActivity(intent)
}

inline fun <reified T : Parcelable> Intent.parcelable(key: String): T? = when {
    android.os.Build.VERSION.SDK_INT >= 33 -> getParcelableExtra(key, T::class.java)
    else -> @Suppress("DEPRECATION") getParcelableExtra(key) as? T
}

fun String?.toTimeAgo(): String {
    if (this.isNullOrEmpty()) return ""
    val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.ENGLISH).apply { timeZone = TimeZone.getTimeZone("UTC") }
    return try {
        val pastDate = sdf.parse(this) ?: return ""
        val diff = Date().time - pastDate.time
        val mins = TimeUnit.MILLISECONDS.toMinutes(diff)
        val hrs = TimeUnit.MILLISECONDS.toHours(diff)
        val days = TimeUnit.MILLISECONDS.toDays(diff)
        when {
            mins < 1 -> "just now"
            mins < 60 -> "$mins minutes ago"
            hrs < 24 -> "$hrs hours ago"
            days < 7 -> "$days days ago"
            else -> SimpleDateFormat("dd MMM yyyy", Locale.ENGLISH).format(pastDate)
        }
    } catch (e: Exception) { "" }
}
""")

with open(f"{core_src_dir}/core/di/NetworkModule.kt", "w") as f:
    f.write("""
package {{package_name}}.core.di
import android.util.Log.d
import com.google.gson.GsonBuilder
import com.google.gson.JsonParser
import {{package_name}}.BuildConfig
import {{package_name}}.core.utils.ConnectivityObserver
import {{package_name}}.core.utils.NetworkMonitor
import {{package_name}}.data.source.remote.ApiService
import dagger.Binds
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class NetworkModule {
    @Binds @Singleton abstract fun bindNetworkMonitor(obs: ConnectivityObserver): NetworkMonitor
    companion object {
        @Provides @Singleton fun provideLoggingInterceptor() = HttpLoggingInterceptor { msg ->
            if (msg.trim().startsWith("{") || msg.trim().startsWith("[")) {
                try {
                    val pretty = GsonBuilder().setPrettyPrinting().create().toJson(JsonParser.parseString(msg))
                    d("OkHttp", pretty)
                } catch (e: Exception) { d("OkHttp", msg) }
            } else d("OkHttp", msg)
        }.apply { level = HttpLoggingInterceptor.Level.BODY }

        @Provides @Singleton fun provideOkHttpClient(log: HttpLoggingInterceptor) = OkHttpClient.Builder()
            .addInterceptor(log)
            .addInterceptor { chain ->
                val url = chain.request().url.newBuilder().addQueryParameter("apiKey", BuildConfig.API_KEY).build()
                chain.proceed(chain.request().newBuilder().url(url).build())
            }.build()

        @Provides @Singleton fun provideRetrofit(client: OkHttpClient) = Retrofit.Builder()
            .baseUrl(BuildConfig.BASE_URL).client(client).addConverterFactory(GsonConverterFactory.create()).build()

        @Provides @Singleton fun provideApiService(r: Retrofit) = r.create(ApiService::class.java)
    }
}
""")

with open(f"{core_src_dir}/core/di/LocalModule.kt", "w") as f:
    f.write("""
package {{package_name}}.core.di
import android.content.Context
import androidx.room.Room
import {{package_name}}.core.Constants
import {{package_name}}.data.source.local.room.database.AppDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object LocalModule {
    @Provides @Singleton fun provideDatabase(@ApplicationContext ctx: Context) =
        Room.databaseBuilder(ctx, AppDatabase::class.java, Constants.DATABASE_NAME).fallbackToDestructiveMigration().build()
    @Provides fun provideDao(db: AppDatabase) = db.appDao()
}
""")

with open(f"{core_src_dir}/core/di/RepositoryModule.kt", "w") as f:
    f.write("""
package {{package_name}}.core.di
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
@Module @InstallIn(SingletonComponent::class) abstract class RepositoryModule { }
""")

with open(f"{core_src_dir}/core/utils/NetworkMonitor.kt", "w") as f:
    f.write("""
package {{package_name}}.core.utils
import android.content.Context
import android.net.*
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.*
import javax.inject.*

interface NetworkMonitor { val isOnline: Flow<Boolean>; suspend fun isCurrentlyOnline(): Boolean }

@Singleton
class ConnectivityObserver @Inject constructor(@ApplicationContext private val context: Context) : NetworkMonitor {
    private val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    override val isOnline: Flow<Boolean> = callbackFlow {
        val callback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(n: Network) { channel.trySend(true) }
            override fun onLost(n: Network) { channel.trySend(false) }
        }
        cm.registerNetworkCallback(NetworkRequest.Builder().addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET).build(), callback)
        channel.trySend(cm.activeNetwork != null)
        awaitClose { cm.unregisterNetworkCallback(callback) }
    }.distinctUntilChanged()
    override suspend fun isCurrentlyOnline(): Boolean = isOnline.first()
}
""")

with open(f"{core_src_dir}/domain/model/Resource.kt", "w") as f:
    f.write("""
package {{package_name}}.domain.model
sealed class Resource<T>(val data: T? = null, val message: String? = null) {
    class Success<T>(data: T) : Resource<T>(data)
    class Loading<T>(data: T? = null) : Resource<T>(data)
    class Error<T>(message: String, data: T? = null) : Resource<T>(data, message)
}
""")

with open(f"{core_src_dir}/data/repository/ResponseHelper.kt", "w") as f:
    f.write("""
package {{package_name}}.data.repository
import com.google.gson.Gson
import com.google.gson.JsonObject
import {{package_name}}.domain.model.Resource
import kotlinx.coroutines.flow.*
import retrofit2.Response

open class ResponseHelper {
    private val gson = Gson()
    protected fun <T> saveApiCall(apiCall: suspend () -> Response<T>) : Flow<Resource<T>> = flow {
        try {
            val response = apiCall()
            if(response.isSuccessful) response.body()?.let { emit(Resource.Success(it)) } ?: emit(Resource.Error("Empty body"))
            else emit(Resource.Error(parseErrorMessage(response.errorBody()?.string(), response.code())))
        } catch (e: Exception){ emit(Resource.Error(e.localizedMessage ?: "Error occurred")) }
    }
    private fun parseErrorMessage(json: String?, code: Int): String {
        if(json.isNullOrBlank()) return "Error: $code"
        return try {
            val obj = gson.fromJson(json, JsonObject::class.java)
            if(obj.has("error")) obj.get("error").asString else json
        } catch (e: Exception){ json }
    }
}
""")

with open(f"{core_src_dir}/data/source/local/room/database/AppDatabase.kt", "w") as f:
    f.write("""
package {{package_name}}.data.source.local.room.database
import androidx.room.*
import {{package_name}}.data.source.local.room.dao.AppDao
@Database(entities = [], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() { abstract fun appDao(): AppDao }
""")

with open(f"{core_src_dir}/data/source/local/room/dao/AppDao.kt", "w") as f:
    f.write("""
package {{package_name}}.data.source.local.room.dao
import androidx.room.Dao
@Dao interface AppDao { }
""")

with open(f"{core_src_dir}/data/source/remote/ApiService.kt", "w") as f:
    f.write("""
package {{package_name}}.data.source.remote
import retrofit2.Response
import retrofit2.http.GET
interface ApiService { @GET("sample") suspend fun getData(): Response<Any> }
""")

with open(f"{core_src_dir}/{{{{app_name.pascalCase()}}}}.kt", "w") as f:
    f.write("""
package {{package_name}}
import android.app.Application
import dagger.hilt.android.HiltAndroidApp
@HiltAndroidApp class {{app_name.pascalCase()}} : Application()
""")

# ---------------------------------------------------------
# BRICK 2: android_feature
# ---------------------------------------------------------
feature_brick = "android_feature"
feature_dir = f"{base_templates_dir}/{feature_brick}/__brick__"
feature_src_dir = f"{feature_dir}/app/src/main/java/{{{{package_name.pathCase()}}}}"
test_src_dir = f"{feature_dir}/app/src/test/java/{{{{package_name.pathCase()}}}}"

create_dir(feature_src_dir)
create_dir(test_src_dir)

with open(f"{base_templates_dir}/{feature_brick}/brick.yaml", "w") as f:
    f.write("""name: android_feature
description: Generate complete feature layers (DTO, Mapper, Domain, UseCase, ViewModel, Test)
version: 1.0.0
vars:
  package_name: { type: string, default: "com.example.app" }
  feature_name: { type: string, default: "News" }
""")

create_dir(f"{feature_src_dir}/data/mapper")
create_dir(f"{feature_src_dir}/data/source/remote/dto")
create_dir(f"{feature_src_dir}/data/repository")
create_dir(f"{feature_src_dir}/domain/model/{{{{feature_name.snakeCase()}}}}")
create_dir(f"{feature_src_dir}/domain/repository")
create_dir(f"{feature_src_dir}/domain/usecase/{{{{feature_name.snakeCase()}}}}")
create_dir(f"{feature_src_dir}/presenter/{{{{feature_name.snakeCase()}}}}")
create_dir(f"{test_src_dir}/data/repository")

with open(f"{feature_src_dir}/data/source/remote/dto/{{{{feature_name.pascalCase()}}}}ResponseDto.kt", "w") as f:
    f.write("""
package {{package_name}}.data.source.remote.dto
import com.google.gson.annotations.SerializedName
data class {{feature_name.pascalCase()}}ResponseDto(
    @field:SerializedName("status") val status: String? = null,
    @field:SerializedName("articles") val articles: List<{{feature_name.pascalCase()}}Dto?>? = null
)
data class {{feature_name.pascalCase()}}Dto(@field:SerializedName("title") val title: String? = null, @field:SerializedName("url") val url: String? = null)
""")

with open(f"{feature_src_dir}/data/mapper/{{{{feature_name.pascalCase()}}}}Mapper.kt", "w") as f:
    f.write("""
package {{package_name}}.data.mapper
import {{package_name}}.data.source.remote.dto.*
import {{package_name}}.domain.model.{{feature_name.snakeCase()}}.*
fun {{feature_name.pascalCase()}}ResponseDto.toDomain() = {{feature_name.pascalCase()}}Result(items = articles.orEmpty().mapNotNull { it?.toDomain() })
fun {{feature_name.pascalCase()}}Dto.toDomain() = {{feature_name.pascalCase()}}(url = url.orEmpty(), title = title)
""")

with open(f"{feature_src_dir}/domain/model/{{{{feature_name.snakeCase()}}}}/{{{{feature_name.pascalCase()}}}}.kt", "w") as f:
    f.write("""
package {{package_name}}.domain.model.{{feature_name.snakeCase()}}
import android.os.Parcelable
import kotlinx.parcelize.Parcelize
@Parcelize data class {{feature_name.pascalCase()}}(val url: String = "", val title: String? = null) : Parcelable
data class {{feature_name.pascalCase()}}Result(val items: List<{{feature_name.pascalCase()}}> = emptyList())
""")

with open(f"{feature_src_dir}/domain/repository/{{{{feature_name.pascalCase()}}}}Repository.kt", "w") as f:
    f.write("""
package {{package_name}}.domain.repository
import {{package_name}}.domain.model.Resource
import {{package_name}}.domain.model.{{feature_name.snakeCase()}}.*
import kotlinx.coroutines.flow.Flow
interface {{feature_name.pascalCase()}}Repository { fun getData(): Flow<Resource<{{feature_name.pascalCase()}}Result>> }
""")

with open(f"{feature_src_dir}/data/repository/{{{{feature_name.pascalCase()}}}}RepositoryImpl.kt", "w") as f:
    f.write("""
package {{package_name}}.data.repository
import {{package_name}}.data.source.remote.ApiService
import {{package_name}}.domain.repository.{{feature_name.pascalCase()}}Repository
import javax.inject.Inject
import {{package_name}}.data.mapper.toDomain
class {{feature_name.pascalCase()}}RepositoryImpl @Inject constructor(private val api: ApiService) : {{feature_name.pascalCase()}}Repository, ResponseHelper() {
    override fun getData() = saveApiCall { api.getData() as retrofit2.Response<{{package_name}}.data.source.remote.dto.{{feature_name.pascalCase()}}ResponseDto> }
}
""")

with open(f"{feature_src_dir}/domain/usecase/{{{{feature_name.snakeCase()}}}}/{{{{feature_name.pascalCase()}}}}UseCases.kt", "w") as f:
    f.write("""
package {{package_name}}.domain.usecase.{{feature_name.snakeCase()}}
import {{package_name}}.domain.repository.{{feature_name.pascalCase()}}Repository
import javax.inject.Inject
class Get{{feature_name.pascalCase()}}UseCase @Inject constructor(private val repo: {{feature_name.pascalCase()}}Repository) {
    operator fun invoke() = repo.getData()
}
""")

with open(f"{feature_src_dir}/presenter/{{{{feature_name.snakeCase()}}}}/{{{{feature_name.pascalCase()}}}}ViewModel.kt", "w") as f:
    f.write("""
package {{package_name}}.presenter.{{feature_name.snakeCase()}}
import androidx.lifecycle.*
import dagger.hilt.android.lifecycle.HiltViewModel
import {{package_name}}.domain.usecase.{{feature_name.snakeCase()}}.*
import javax.inject.Inject
@HiltViewModel class {{feature_name.pascalCase()}}ViewModel @Inject constructor(private val getUseCase: Get{{feature_name.pascalCase()}}UseCase) : ViewModel() { }
""")

with open(f"{test_src_dir}/data/repository/{{{{feature_name.pascalCase()}}}}RepositoryImplTest.kt", "w") as f:
    f.write("""
package {{package_name}}.data.repository
import {{package_name}}.core.di.NetworkModule
import kotlinx.coroutines.test.runTest
import okhttp3.logging.HttpLoggingInterceptor
import org.junit.*
class {{feature_name.pascalCase()}}RepositoryImplTest {
    private lateinit var repository: {{feature_name.pascalCase()}}RepositoryImpl
    @Before fun setup() {
        val log = HttpLoggingInterceptor {}.apply { level = HttpLoggingInterceptor.Level.NONE }
        val api = NetworkModule.provideApiService(NetworkModule.provideRetrofit(NetworkModule.provideOkHttpClient(log)))
        repository = {{feature_name.pascalCase()}}RepositoryImpl(api)
    }
    @Test fun testFetch() = runTest { }
}
""")

print(f"✅ Completed! Standalone brick with full Gradle setup has been created at {base_templates_dir}!")