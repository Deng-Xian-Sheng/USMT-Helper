Claude，你现在即将进行与编程有关的任务，编程语言是Python。

我已经将代码给你，由一个配置文件 migrate_config.toml 和 一个主程序文件 migrate.py 组成

项目概述：这是一个在Windows系统中，用来复制文件和注册表的Python程序。注意是复制而不是移动，但是在项目中很多地方都会使用“迁移”这个词，项目本身也是用来“迁移”Windows系统中的应用程序到另一个Windows系统的，不过“用来迁移Windows系统中的应用程序到另一个Windows系统”这种说法是一种让非开发人员能够理解的说法，不够具体，也不应将其与代码实现联系起来。回到关于“迁移”的解释中，是复制而不是移动，但是在项目中很多地方都会使用“迁移”这个词，这只是为了迎合非开发人员对程序的理解，你可以理解为“迁移”但是不会改动源，其实就是复制。

项目进度概述：复制文件的部分已经实现好了，不要改动它，除非它影响了复制注册表的实现，即使改动它也要确保复制文件的功能不变且可用。

代码文件概述： migrate_config.toml 里面定义了用来复制文件和注册表所需的参数，这些参数由人为配置，随使用者的具体需求和意愿去调整。其中，复制文件的参数已经定义完成了。复制注册表的参数定义了一个框架，还没有具体定义。

migrate.py 里面是读取配置文件和复制文件和注册表的具体代码实现。其中，读取配置文件和复制文件的代码已经编写完成了。复制注册表的代码还没有实现。

你的任务：实现项目中的功能之一“复制注册表”。你需要在 migrate_config.toml 文件中定义复制注册表的所需参数，在 migrate.py 文件中实现复制注册表的具体代码。我能给你的只有一些想法，我也不知道具体怎么做，你得自己解决。我的想法是这样的，在winreg库中有些名词，“键”和“值”，键相当于注册表路径，值是某个路径里面的东西，但是值其实也有名字，也有类型，也有值。而路径下还有子路径，子路径里面也有值。我把键和值作为一个对，通过 glob 风格的一对（键和值）作为要复制的东西或要排除的东西的配置文件参数。也就是说，键和值作为一对，并且使用 glob​ 风格，共同决定复制或排除的东西。

开始干吧！