Note to self:

- In kubernetes manifest the sector and the template label->app text must match
- the selector names are immutable within the context if a deployment metadata-name.
- That is to say that after you make a deployment all the following "update" deployments must use the same naming structure in the selector section
- The selector->app value on the service must mathc the selector->matchLabel->app on the template/selector
- 