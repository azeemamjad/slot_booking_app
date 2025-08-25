from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut, DepartmentDeleteResponse


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_departments(self, skip: int = 0, limit: int = 100) -> List[DepartmentOut]:
        """Get all departments with pagination."""
        query = select(Department).options(
            selectinload(Department.users)
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        departments = result.scalars().all()
        
        return [DepartmentOut.from_orm(department) for department in departments]

    async def get_department_by_id(self, department_id: int) -> DepartmentOut:
        """Get a specific department by ID."""
        query = select(Department).options(
            selectinload(Department.users)
        ).where(Department.id == department_id)
        
        result = await self.db.execute(query)
        department = result.scalars().first()
        
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        return DepartmentOut.from_orm(department)

    async def get_department_by_title(self, title: str) -> Optional[Department]:
        """Get department by title (for internal use)."""
        query = select(Department).where(Department.title == title)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_department(self, department_data: DepartmentCreate) -> DepartmentOut:
        """Create a new department."""
        # Check if title already exists
        existing_department = await self.get_department_by_title(department_data.title)
        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department with this title already exists"
            )
        
        # Create department object
        department = Department(
            title=department_data.title,
            description=department_data.description
        )
        
        self.db.add(department)
        await self.db.commit()
        await self.db.refresh(department)
        
        # Load relationships for response
        await self.db.refresh(department, ["users"])
        
        return DepartmentOut.from_orm(department)

    async def update_department(self, department_id: int, department_data: DepartmentUpdate) -> DepartmentOut:
        """Update an existing department."""
        # Get the department
        query = select(Department).where(Department.id == department_id)
        result = await self.db.execute(query)
        department = result.scalars().first()
        
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        # Check if new title conflicts with existing department
        if department_data.title and department_data.title != department.title:
            existing_department = await self.get_department_by_title(department_data.title)
            if existing_department:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Department with this title already exists"
                )
        
        # Update fields
        if department_data.title is not None:
            department.title = department_data.title
        if department_data.description is not None:
            department.description = department_data.description
        
        await self.db.commit()
        await self.db.refresh(department)
        
        # Load relationships for response
        await self.db.refresh(department, ["users"])
        
        return DepartmentOut.from_orm(department)

    async def delete_department(self, department_id: int) -> DepartmentDeleteResponse:
        """Delete a department."""
        # Get the department
        query = select(Department).options(
            selectinload(Department.users)
        ).where(Department.id == department_id)
        result = await self.db.execute(query)
        department = result.scalars().first()
        
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        # Check if department has users
        if department.users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete department with existing users. Please reassign or delete users first."
            )
        
        await self.db.delete(department)
        await self.db.commit()
        
        return DepartmentDeleteResponse(message="Department deleted successfully")
