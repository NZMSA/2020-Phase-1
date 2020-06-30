# Table of contents
1. [API and Databases](#api-and-databases)
2. [Model](#model)
3. [Azure Database](#azure-database)
4. [Time to Code - Model and Context Creation](#model-and-context-creations)
5. [Time to Code - Migrations](#migrations)
6. [Time to Code - API Controllers](#api-controllers)
7. [Time to Code - Swagger](#swagger)
8. [Time to Code - Updating our model](#update-model)
9. [Deploy .NET Core Web API to Azure](#deployment)
10. [Assignments](#assignments)

# API and Databases <a name="api-and-databases"></a>

API forms the layer between our front-end and database. The API handles the logic when a request is received by or sent from the front-end.

## 1. Before you Start
Here are the required things to get/install for the project:
- Visual Studio 2019
- .NET Core 3.1
- Azure Account with active subscription. Microsoft Azure for Students [(Documentation can be found here)](https://github.com/NZMSA/2019-Phase-1/tree/master/Azure%20For%20Students)
- Git

## Video tutorial
[Our database + RESTful API video tutorial could be found here](https://youtu.be/ALHU7LkpCTA)

### 1.1 Learning Outcomes
- Creating a database hosted on Azure.
- Using **Code First** programming to design our system (If you are interested you can see [NZMSA 2019](https://github.com/NZMSA/2019-Phase-1/tree/master/Databases%20%26%20API) for the database first approach)
	- **Add** tables remotely through code without SQL
	- **Update** database to reflect model in code without SQL
- Creating an API that performs CRUD operations.
- Understanding the interactions with API and Databases.

### 1.2 Why API and Database

API (Application Programming Interface) defines the interactions between the client (front-end) and the server (backend/database). From [WikiPedia](https://en.wikipedia.org/wiki/Application_programming_interface):

> It defines the kinds of calls or requests that can be made, how to make them, the data formats that should be used, the conventions to follow, etc.

It is helpful because it makes our (the developers') life easier. Because it adds a **layer of abstraction** between the client and the server, the developer **does not** have to write *low-level* code that makes the direct interactions anymore. We use the methods exposed by the API. For example, suppose we want to retrieve all employees whose age are under 30 from a database to our front-end. **Without an API**, we will write:

```c#
// pseudo-code
SQL sql = new SQL()
string query = "SELECT * FROM employee WHERE employee.age < 30"
Employee[] employees = sql.query(query)

foreach (Employee e in employees) {
    // render the employee in the frontend
}
```

However, **with an API**, we do not have to write sql to query the data anymore:

```c#
Employee[] employees = database.getEmployees(e => e.age < 30>)

foreach (Employee e in employees) {
    // render the employee in the frontend
}
```

In the above over-simplified demonstration, you may not see the immediate advantage of using the API. However, when the business logic grows larger or our application becomes more complex, the **API allows** us to directly act without the need to write the low-level query code repeatedly.

There is a small documentations on interaction between Database and API [here](DB-API.md). Have a look at it if you are still not sure how they work together.

# 2. Model <a name="model"></a>

Before we even start to write a line of code, we need to think about what we would like to store in our database and what properties we want our API to return (i.e. **the Model**). The model is crucial because the **cost of modifying** an existing database is *very high*. To keep it simple, we will only have one table and one model. Be aware that in the modern system that multiple models can exist that pull data from various databases.

Now we can design the model. Here we will create a database that holds students' details. Our model will have the following fields:

- StudentId
- First Name
- Last Name
- Email Address

The model seems simple but later we will start updating it to make things more complex and fun.

# 3. Azure Database <a name="azure-database"></a>
Before we can build our model we first need a server to host our database. There are multiple ways and technologies we could use to create a database. For simplicity we will use Azure SQL databases to host our data. For this step you will need a Azure for Student Subscription and an account to go with it. Visit [https://azure.microsoft.com/en-us/free/students/](https://azure.microsoft.com/en-us/free/students/) to redeem your subscription. This will give you some free credits to host our API and Databases.

### 3.1 Creating the database

Navigate to https://portal.azure.com on your browser and click **Create a resource** and search for **SQL Database**.

![Create Resource](./img/Azure%20%281%29.png)

> Make sure the subscription is Azure for Students.

- Click **Create New**, to create a new resource group. (The resource group is a collection of resources that are used for a particular application or group of applications)

![Create Resource Group](./img/Azure%20%282%29.png)

- Name your database.

![db name](./img/Azure%20%284%29.png)

- Click **Create new** which will prompt you to create a admin account for this database and the select a region that it will be hosted on.

![SQL admin](./img/Azure%20%285%29.png)

- You should have something similar to this.

![settings](./img/Azure%20%286%29.png)

- Click **Configure database** and navigate to the basic option (the default one is overkill and is quite expensive for our purposes) and apply the changes.

![config database](./img/Azure%20%287%29.png)

![config database](./img/Azure%20%288%29.png)

> We want to change the database configuration because the default one is expensive and an overkill for our purposes. (Cost $641 for me to host the default monthly)

![config database](./img/Azure%20%289%29.png)

> Way cheaper cost only $8 a month, be sure to delete the database after the phase 1 results are given out so that it doesn't eat into your credits.

Once satisfied with the setting you can click review and create and the deployment should be underway. This might take some time.

![Create Resource](./img/Azure%20%2810%29.png)

### 3.2 Firewall settings
When the database has finished being deployed you can click on "Go to resource" and 'Set server firewall'.

![Firewall](./img/Azure%20%2811%29.png)

![Firewall](./img/Azure%20%2812%29.png)

Change the setting so that 'Allow Azure service' is Yes and add the rule 0.0.0.0 and 255.255.255.255. This is giving all IP addresses access. Ideally we would want to restrict access in a production environment but for simplicity I will allow all connections.

![Allow All](./img/Azure%20%2813%29.png)

On the left hand panel find the label **Connection String** and copy the string somewhere. (We would need this to connect to the database we created in the `.NET` project)

![Connection String](./img/Azure%20%2814%29.png)

Copy the **connection string** under ADO.NET.

![Copy String](./img/Azure%20%2815%29.png)

# 4. Time to Code – Model and context creations <a name="model-and-context-creations"></a>
### 4.1 Creating a new web API project
Open Visual Studio 2019 -> Create a new Project -> ASP.NET Core Web Application

![Create app](./img/api%20%281%29.png)

Give your project a name.

![project name](./img/api%20%282%29.png)

Select API -> Click **Create**

![Api](./img/api%20%283%29.png)

We have created an empty API project which will will create our core logic of our API. At this point you can Click **IIS Express** to run the project. The newly created API project comes with a default API `WeatherForecastController.cs`, It should show you the following data.

![run api](./img/api%20%284%29.png)

![output json](./img/api%20%285%29.png)

Now that we know the project runs we can delete the `WeatherForecast.cs` and the `WeatherForecastController.cs` by right clicking them and selecting **delete** in the **Solution Explorer** - the panel on the right-hand side of the VS editor.

![delete default](./img/api%20%287%29.png)

### 4.2 Adding Nuget Packages
We also need to install some libraries/extensions to the project to help us create the API.
At the top of the screen go to **Tools** -> **Nuget Package Manager** -> **Manage Nuget Package for Solution**.

![nuget manager](./img/api%20%288%29.png)

Click browse and search for `Microsoft.EntityFrameworkCore`, add and install it. This framework is an ORM (Object-Relational Mapper) that allows developers to work with a database using `.NET` objects. More in the [Microsoft Doc](https://docs.microsoft.com/en-us/ef/core/#:~:text=Entity%20Framework%20(EF)%20Core%20is,work%20with%20a%20database%20using%20.).

![install packages](./img/api%20%289%29.png)

Do the same to add and install:
- `Microsoft.EntityFrameworkCore.Tools` (**Migration**)
- `Microsoft.EntityFrameworkCore.SqlServer` (**database communication**)

### 4.3 Adding the Model
Right click the `Models` folder and select **add new item**.

![model](./img/api%20%2810%29.png)

![add item](./img/api%20%2811%29.png)

> Give your class file a name. This class will be our model for our student data.
Under the `Student.cs` class add the follow code. The `Student` class has the 4 attributes which we define earlier for the database, namely `studentId`, `firstName`, `lastName` and `emailAddress`. Notice each attribute also has a `get` and `set` method respectively, this allow us to read and update the respective values later on. `[Key]` and `[DatabaseGenerated(DatabaseGeneratedOption.Identity)]` are explained below.

```C#
    public class Student
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int studentId { get; set; }
        public string firstName { get; set; }
        public string lastName { get; set; }
        public string emailAddress { get; set; }
    }
```

![model code](./img/api%20%2812%29.png)

You will see that Visual Studio complaining about an error. We can fix this by hovering over or clicking the lightbulb icon to show potential fixes. In our case we want to import the following.

- `using System.ComponentModel.DataAnnotations;`
- `using System.ComponentModel.DataAnnotations.Schema;`

![fix using snippet](./img/api%20%2813%29.png)

![fix using snippet](./img/api%20%2814%29.png)

This imports the libraries that we added and installed previously.

> `[Key]` denotes the primary Id that is used to identify the row of data. This  annotation isn’t strictly needed if your variable has Id in the name, because by convention, a property named Id or `<type name>`Id will be configured as the **primary key** of an entity.

> `[DatabaseGenerated(DatabaseGeneratedOption.Identity)]` annotation tells the database that we want this attributed to be automatically generated when we add a `Student` to the database and it is the primary identifier. More information can be found [here](https://docs.microsoft.com/en-us/ef/core/modeling/entity-properties?tabs=data-annotations,without-nrt)

We are now done with our basic model!

### 4.4 Adding the DbContext

**DbContext** is *the way* to incorporate EntityFramework-based data access into the application. In other words, the class that derives or is registered with DbContext is the data access layer of the application.

> More information on **DbContext** [here](https://docs.microsoft.com/en-us/dotnet/api/system.data.entity.dbcontext?view=entity-framework-6.2.0)

Right click the project and create a new folder called `Data`. In this new folder, create a new file called `StudentContext.cs`, Add the following code to the file and fix all the errors using the suggested solutions prompted by the lightbulb.

```C#
public class StudentContext : DbContext
    {
        // an empty constructor
        public StudentContext() {}

        // base(options) calls the base class's constructor,
        // in this case, our base class is DbContext
        public StudentContext(DbContextOptions<StudentContext> options) : base(options) {}

        // Use DbSet<Student> to query or read and 
        // write information about A Student
        public DbSet<Student> Student { get; set; }
        public static System.Collections.Specialized.NameValueCollection AppSettings { get; }

        // configure the database to be used by this context
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            IConfigurationRoot configuration = new ConfigurationBuilder()
           .SetBasePath(AppDomain.CurrentDomain.BaseDirectory)
           .AddJsonFile("appsettings.json")
           .Build();

           // schoolSIMSConnection is the name of the key that
           // contains the has the connection string as the value
            optionsBuilder.UseSqlServer(configuration.GetConnectionString("schoolSIMSConnection"));
        }
    }
```

![Context](./img/api%20%2815%29.png)

![Context](./img/api%20%2816%29.png)

# 5. Time to Code – Migrations
Now that we have set up our model and the context, we can begin to update the database with our model. Code first programming will allow us to mirror our model in our database. First remember we had the connection previously when we created our database. Open `appsettings.json` and add the following. (where **CONNECTIONSTRING** is the string you copied earlier when we created the database in Azure Portal)

```JSON
"AllowedHosts": "*",
"ConnectionStrings": {
    "schoolSIMSConnection": "CONNECTIONSTRING"
  }
```

![conn string add](./img/api%20%2817%29.png)

> Make sure you replace `{your_password}` with your admin password in the connection string you copied

At the bottom of the screen click package console manager, run the following command `Add-Migration InitialCreate`. The command creates files needed to update the database. A folder called `Migration` will be created, it has a record or all migrations we have made. In other words, when we change the schema of the database, e.g. if we rename or drop a column, without migration, all data is lost upon update of the schema, but with migration, not only it updates the schema of the database but it also preserves the existing data. Essentially it is git for the model. (More info on [Migration](https://docs.microsoft.com/en-us/ef/core/managing-schemas/migrations/?tabs=dotnet-core-cli#:~:text=The%20migrations%20feature%20in%20EF,Create%20a%20migration.) can be found here)

![add-migrations](./img/api%20%2818%29.png)

![add-migrations](./img/api%20%2819%29.png)

We haven’t updated the remote database yet but running the command `Update-Database` will create the model on our database.

Go back to Azure and find your database and select the `Query Editor` on the left hand panel, log in and expand the Tables folder. 

![table updated](./img/api%20%2820%29.png)

You can see two tables. one is a record of the migrations we have made and the other is the table for your model. You have successfully updated the database using code first approach. If you want to know how to do database first take a look at the last years API and Databases [here](https://github.com/NZMSA/2019-Phase-1/tree/master/Databases%20&%20API).

# 6. Time to Code – API Controllers <a name="api-controllers"></a>
> The controller is where all our api’s are created. To create basic API we will use scaffolding which will give us some API that is automatically created.

> The **controller** is where all our api’s are created. To create basic API we will use **scaffolding** which automatically creates some API methods.

Open `Startup.cs` and add the following code to the `ConfigureServices` method, replacing the string `schoolSIMSConnection` with the connection string name you have in `appsettings.json` (i.e. in `appsettings.json`, use `YOUR_CONNECTION_STRING_NAME` found in `"ConnectionStrings": { "YOUR_CONNECTION_STRING_NAME": "...." }`)

 ```C# 
var connection = Configuration.GetConnectionString("schoolSIMSConnection");
services.AddDbContext<StudentContext>(options => options.UseSqlServer(connection));}
```

> This adds the dbContext to our program.

Right click the `Controllers` folder and select **Add** -> **New Scaffold Item** -> **Select API Controller with actions, using Entity Framework**. Here select your model and context you create previously.

![scaffolding nav](./img/api%20%2821%29.png)

![Api controller with](./img/api%20%2822%29.png)

![model and context](./img/api%20%2823%29.png)

![results](./img/api%20%2824%29.png)

> This generates the API methods. This is very basic api but it will give us the some boiler plate code to work with. You can run then program again but go to one of the api/Students.

This isn’t very visual pleasing to work with so we will use Swagger UI to visualize and interact with the API's in the next step.

# 7. Time to Code – Swagger. <a name="swagger"></a>
### 7.1 Setting up Swagger
Install the nuget package Swashbuckle.AspNetCore

Install the nuget package **Swashbuckle.AspNetCore**

Add the following code to `ConfigureServices` in `Startup.cs` and fix the errors using the suggestions from the lightbulb in the VS editor.

```C#
services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "StudentSIMS", Version = "v1" });
});
```

Add the following to `Configure`:

```C#
app.UseSwagger();
// Enable middleware to serve swagger-ui (HTML, JS, CSS, etc.),
// specifying the Swagger JSON endpoint.
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "My first API V1");
    c.RoutePrefix = string.Empty; // launch swagger from root
});
```

In `Properties/launchsetting.json` edit the launchUrl to be `""`.

Run the program and go to the prompted localhost url in the console, then you should be greeted with a nice Swagger UI.

![swagger ui](./img/api%20%2825%29.png)

### 7.2 Testing our API
Time to see if our API is working.

Click on **POST api/Students** and click **Try it out**

![post](./img/api%20%2828%29.png)

> POST is a HTTP method used to send data to a server to create a new record.

Edit the fields to fill out the first name, last name and email. It doesn't matter what StudentId is because it will be auto-generated for us. (Recall the primary key `studentId` has an attribute `[DatabaseGenerated(DatabaseGeneratedOption.Identity)]` defined in our schema in `Student.cs`)

![edit post](./img/api%20%2826%29.png)

Click **Execute**, if the response is `201` then we have successfully added some data to our database. See [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) for common HTTP response codes.

![response](./img/api%20%2827%29.png)

We can check if our data was added in our database by this executing **GET api/students**, the API is fully functional if it responds with a 200 success code as shown in the image below.

![get](./img/api%20%2829%29.png)

# 8. Time to Code – Updating our model <a name="update-model"></a>
If your model needs to change, we simply update the existing model. We will add a timestamp, a phone number and a middle name. We will also make the first and last name the required fields, and impose a max length on the first name field. (Click [here](https://docs.microsoft.com/en-us/ef/core/modeling/entity-properties?tabs=data-annotations,without-nrt) to see more data annotations you can apply to the model)
```C#
public class Student
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int studentId { get; set; }
        [Required, MaxLength(100)]
        public string firstName { get; set; }
        public string middleName { get; set; }
        [Required]
        public string lastName { get; set; }
        public string emailAddress { get; set; }
        public int phoneNumber { get; set; }
        [Timestamp]
        public DateTime timeCreated { get; set; }
    }
```

![migration update](./img/api%20%2830%29.png)

Go to package manger console and run `Add-Migration UpdatedStudentModel` and `Update-Database`.

If you make a mistake with the model, you can roll back to the previous version by calling `Update-Database` with the name of the previous migration. Take a look [here](https://docs.microsoft.com/en-us/ef/core/managing-schemas/migrations/?tabs=vs#remove-a-migration) and [here](https://docs.microsoft.com/en-us/ef/core/managing-schemas/migrations/?tabs=dotnet-core-cli) for more Migration functionality.

# 9. Deploy .NET Core Web API to Azure <a name="deployment"></a>
Now we will deploy our finished .NET CORE Web API to Azure.

## 9.1 Development Environment
1. Visual Studio Community 2019, version 16.6.2
2. .NET CORE 3.1
3. Azure Student Subscription

## 9.2 Configure CORS
Firstly, we will configure the application to enable CORS policy so that we can host it on Azure with Swagger UI.

In Visual Studio, go to your `Startup.cs` file and update the Configure and ConfigureServices methods as below:
``` csharp
public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {      
       app.UseCors(builder => builder
                .AllowAnyHeader()
                .AllowAnyMethod()
                .SetIsOriginAllowed((host) => true)
                .AllowCredentials()
            );
    }

    public void ConfigureServices(IServiceCollection services)
    {
        services.AddCors();
    }
```

Your two methods then will be look like:

![Configure CORS](./img/configure-cors.PNG)

## 9.3 Deployment
In order to deploy our .NET Core Application to Azure, we need an Azure account with subscription. If you are a student, you can register a student subscription with Microsoft Azure.
Once you are ready with your Azure account, login into [Azure](http://portal.azure.com/) and search for "App Services"

From "App Services", we choose the "Add" to create a new App Service.

![Add App Services](./img/add-app-services.PNG)

Then we need to fill out the following fields:

![Web App Form](./img/web-app-form.PNG)

- **Subscription**: Choose "Azure for Students" if you are a student and have registered for the student subscription with Azure
- **Resource Group**: is a container that holds related resources for an Azure solution. If you don’t have existing resource group, you can click “Create new” to create one.
- **Name**: this would be your app’s name.
- **Publish**: I will choose the code option.
- **Runtime Stack**: select the correct runtime stack. For example, in this tutorial, we are using .NET Core 3.1, so I will select .NET Core 3.1.
- **Region**: select the correct region.
- **Plan**: leave as default
- **Sku and size**: Here I choose Free F1 option.

Then choose `Review and Create`, check for your configurations, and select `Create`.

Azure will then deploy your empty app to Azure server.

After we have configured the web service on Azure, we are now move to deploy our .NET Core Web API code to Azure.

Now go back to your Visual Studio, right click your API project and choose `Publish...`

![Choose Publish](./img/choose-publish.png)

Then choose `Azure` as our `Target` to publish

![Where to Publish](./img/where-publish.PNG)

For `Specific target`, we choose `Azure App Service(Windows)`

![Windows Publish](./img/windows-publish.PNG)

For `App Service`, we will choose the existing Azure App Service that we have just created. Make sure that you are logged in the correct account from which you created the App Service. Select the correct `Subscription` and the `App Service`

![Existing Publish](./img/existing-publish.PNG)

And then select `Finish`

In the Publish window, check to ensure that all configurations are correct. Then select `Publish` to publish your code to the existing Azure App Service.

![Publish Code](./img/publish-code.PNG)

When it is published successfully, it will automatically open up the site, else you can click the `Site URL` to open it in browser and test if your APIs work well.

![Successful Deployed](./img/successful-deployed.PNG)

Hosting APIs on Azure will allow you to call the APIs anytime on any devices. For example, developers use YouTube or Google APIs to build their applications.

# 10. Assignments for API + Database module <a name="assignments"></a>

## 10.1 Submission

Students will need to submit a link to GitHub repository. Your `README.md` should contain the following contents, refer to 10.2 for more details:

- All the screenshots and explanations/notes
- URLs of your APIs that have been hosted on Azure

## 10.2 Project Guidelines

- Create a **code-first** API server with Azure SQL Database
  - Database:
    - Create another table named **Address** with attributes: `StudentId`, `Street Number`, `Street`, `Suburb`, `City`, `Postcode` and `Country`. The **Student** table would have a one-to-many relationship with this table. Please assign appropriate datatype (i.e. `string`, `int` etc.) for each of the attributes.
    - Show SQL database through the Query editor (**screenshots**) for both tables with rows of example instances

  - API manipulate the created Azure Database using Code-First migration:
    - Create basic CRUD requests for the **Student** and **Address** table.
    - Create an API method that **adds** new address for a student using his/her StudentId.
    - Create an API method that **changes** the address of a student using his/her StudentId.
    - **Screenshot** of Swagger UI showing all API Endpoints

- Microsoft Learn Module
  - Student will need to finish 1 compulsory :
    - Compulsory: [Create a web API with ASP.NET Core](https://docs.microsoft.com/en-us/learn/modules/build-web-api-net-core/?fbclid=IwAR0YijdrKtl3UUkQLVTUw3i6RTJbkxLte7RbZhD2aBPYvZva-Pp-_WRYbJM)
    - Optional module that will help you with your learning:
      - [Provision an Azure SQL database to store application data](https://docs.microsoft.com/en-us/learn/modules/provision-azure-sql-db/?fbclid=IwAR0k7zN0rgLgISyDoSZP7l3Mm1nEUjUY9nJJS0TnVEPjdn78xzWThfJesLk)
      - [Develop and configure an ASP.NET application that queries an Azure SQL database](https://docs.microsoft.com/en-us/learn/modules/develop-app-that-queries-azure-sql/?fbclid=IwAR2j2JDWm8dfkpOV8T-QYu6M1VHw6cFgvRBYF03K_ZXUerX2HJ28O2OUWBo)

